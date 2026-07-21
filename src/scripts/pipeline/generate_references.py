#!/usr/bin/env python3
"""Generate references/{market}-endpoints.jsonl from schema/sectors-api.source.json.

Idempotent: same schema in -> byte-identical JSONL out. Run after every
schema update and commit the diff (see README.md).

Key convention:
- Key = the operation's `summary` field, verbatim. It's already the
  schema author's canonical human-facing name for the operation, so no
  normalization logic is needed.
- The schema declares a handful of duplicate paths for the same operation
  (a `path`-parameter declared on a URL with no matching `{name}` -- a
  documentation artifact). Those phantom-duplicate paths are skipped
  before key assignment; this is also what keeps `summary` collision-free
  (the only `summary` duplicates in the raw schema are exactly these
  phantom pairs).
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parent.parent.parent

_ENV_PATH = SRC_ROOT / ".env"
if _ENV_PATH.exists():
    for _line in _ENV_PATH.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

SCHEMA_PATH = SRC_ROOT / "schema" / "sectors-api.source.json"
REFERENCES_DIR = SRC_ROOT / "references"
OVERRIDES_PATH = SRC_ROOT / "scripts" / "data" / "overrides.json"

MARKET_BY_TAG_GROUP = {
    "Indonesia (IDX)": "idx",
    "Singapore (SGX)": "sgx",
    "Malaysia (KLSE)": "klse",
    "Mining (Extension)": "mining",
}


def resolve_schema(schema, components, depth=0, seen=frozenset()):
    """Turn an OpenAPI schema (possibly $ref) into a compact type tree."""
    if depth > 4:
        return "..."
    if "$ref" in schema:
        name = schema["$ref"].rsplit("/", 1)[-1]
        if name in seen:
            return f"ref:{name}"
        target = components.get("schemas", {}).get(name, {})
        return resolve_schema(target, components, depth, seen | {name})

    schema_type = schema.get("type")
    if schema_type == "array":
        items = schema.get("items")
        return [resolve_schema(items, components, depth + 1, seen)] if items else []
    if schema_type == "object" or "properties" in schema:
        props = schema.get("properties")
        if not props:
            return "object"  # free-form (additionalProperties: {}), see `example`
        return {k: resolve_schema(v, components, depth + 1, seen) for k, v in props.items()}

    out = schema_type or "any"
    if schema.get("nullable"):
        out += "|null"
    if schema.get("format"):
        out += f"({schema['format']})"
    if "enum" in schema:
        out += f" enum{schema['enum']}"
    return out


def build_response(operation, components):
    ok = operation.get("responses", {}).get("200")
    if not ok:
        return None
    content = ok.get("content", {}).get("application/json", {})
    schema = content.get("schema")
    example = None
    examples = content.get("examples")
    if examples:
        first = next(iter(examples.values()))
        example = first.get("value")
    return {
        "schema": resolve_schema(schema, components) if schema else None,
        "example": example,
    }


def build_params(operation):
    params = []
    for p in operation.get("parameters", []):
        schema = p.get("schema", {})
        entry = {
            "name": p["name"],
            "in": p["in"],
            "type": schema.get("type"),
            "required": p.get("required", False),
            "description": p.get("description"),
        }
        if "default" in schema:
            entry["default"] = schema["default"]
        if "enum" in schema:
            entry["enum"] = schema["enum"]
        params.append(entry)
    return params


def has_phantom_path_param(path, operation):
    """True if a declared `in: path` param has no matching `{name}` in the URL.

    This flags the schema's duplicate query-vs-path-param entries for the
    same logical operation; the phantom one is skipped in favor of the
    real path-templated URL.
    """
    url_placeholders = set(re.findall(r"\{(\w+)\}", path))
    declared = {p["name"] for p in operation.get("parameters", []) if p.get("in") == "path"}
    return bool(declared - url_placeholders)


def load_overrides():
    if OVERRIDES_PATH.exists():
        return json.loads(OVERRIDES_PATH.read_text())
    return {}


def load_schema():
    """Return parsed schema JSON. Prefer local file, fall back to download."""
    if SCHEMA_PATH.exists():
        return json.loads(SCHEMA_PATH.read_text())
    try:
        url = os.environ["SCHEMA_SOURCE_URL"]
    except KeyError:
        print("ERROR: SCHEMA_SOURCE_URL must be set in .env", file=sys.stderr)
        sys.exit(1)
    print(f"Fetching schema from {url} ...")
    resp = urllib.request.urlopen(url, timeout=30)
    schema = json.loads(resp.read().decode())
    SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCHEMA_PATH.write_text(json.dumps(schema, indent=2))
    print(f"  {len(schema['paths'])} paths -> {SCHEMA_PATH}")
    return schema


def main():
    schema = load_schema()
    components = schema.get("components", {})
    overrides = load_overrides()

    tag_to_market = {}
    for group in schema["info"]["x-tagGroups"]:
        market = MARKET_BY_TAG_GROUP[group["name"]]
        for tag in group["tags"]:
            tag_to_market[tag] = market

    kept = {
        path: item["get"]
        for path, item in schema["paths"].items()
        if "get" in item and not has_phantom_path_param(path, item["get"])
    }

    by_market = {m: [] for m in MARKET_BY_TAG_GROUP.values()}
    for path, operation in kept.items():
        key = operation["summary"]
        tags = operation.get("tags", [])
        market = tag_to_market[tags[0]]

        entry = {
            "key": key,
            "path": path,
            "method": "GET",
            "summary": operation.get("summary"),
            "description": operation.get("description"),
            "params": build_params(operation),
            "response": build_response(operation, components),
        }
        entry.update(overrides.get(key, {}))
        by_market[market].append(entry)

    REFERENCES_DIR.mkdir(exist_ok=True)
    for market, entries in by_market.items():
        entries.sort(key=lambda e: e["key"])
        out_path = REFERENCES_DIR / f"{market}-endpoints.jsonl"
        lines = [json.dumps(e, sort_keys=True, ensure_ascii=False) for e in entries]
        out_path.write_text("\n".join(lines) + "\n" if lines else "")
        print(f"{out_path.relative_to(SRC_ROOT)}: {len(entries)} endpoints")


if __name__ == "__main__":
    sys.exit(main())
