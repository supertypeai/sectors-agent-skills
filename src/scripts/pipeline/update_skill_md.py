#!/usr/bin/env python3
"""Generate the decision table in SKILL.md from schema + intent map.

Finds `<!-- GENERATED:decision-table:start -->` / `:end -->` markers in each
target SKILL.md and replaces the content between them with a flat table
derived from the schema and the hand-authored intent map.

Idempotent: run twice → no diff.

Usage:
    python scripts/update_skill_md.py              # update both SKILL.md files
    python scripts/update_skill_md.py SKILL.md     # update a single file
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_PATH = SRC_ROOT / "schema" / "sectors-api.source.json"
SCHEMA_URL = os.environ.get("SCHEMA_SOURCE_URL")
INTENT_MAP_PATH = SRC_ROOT / "scripts" / "data" / "intent_map.json"
MARKER_START = "<!-- GENERATED:decision-table:start -->"
MARKER_END = "<!-- GENERATED:decision-table:end -->"

MARKET_BY_TAG_GROUP = {
    "Indonesia (IDX)": "idx",
    "Singapore (SGX)": "sgx",
    "Malaysia (KLSE)": "klse",
    "Mining (Extension)": "mining",
}
MARKET_LABEL = {"idx": "IDX", "sgx": "SGX", "klse": "KLSE", "mining": "Mining"}
MARKET_ORDER = {"IDX": 0, "SGX": 1, "KLSE": 2, "Mining": 3}

# Order for sorting within each market — matches schema's x-tagGroups order
TAG_ORDER = [
    "Company Screener", "Helper Lists", "Detailed Reports",
    "Transaction Data", "Rankings", "IPO & Performance",
    "News & Filings", "Brokers",
    "SGX - Company Screener", "SGX - Helper Lists",
    "SGX - Detailed Reports", "SGX - Transaction Data",
    "SGX - Rankings", "SGX - News & Filings",
    "KLSE",
    "Companies", "Commodities & Trade", "Production & Sites",
    "Contracts & Licenses",
]
TAG_ORDER_IDX = {t: i for i, t in enumerate(TAG_ORDER)}


def load_intent_map():
    if INTENT_MAP_PATH.exists():
        return json.loads(INTENT_MAP_PATH.read_text())
    return {}


def has_phantom_path_param(path, operation):
    url_placeholders = set(re.findall(r"\{(\w+)\}", path))
    declared = {p["name"] for p in operation.get("parameters", []) if p.get("in") == "path"}
    return bool(declared - url_placeholders)


def required_params(operation):
    """Return comma-separated string of required param names, or 'none'."""
    names = [p["name"] for p in operation.get("parameters", []) if p.get("required")]
    if not names:
        return "none"
    return ", ".join(f"`{n}`" for n in names)


def market_tag(operation, tag_to_market):
    """Return (market_label, tag_name) for this operation."""
    tags = operation.get("tags", [])
    if not tags:
        return ("IDX", "Helper Lists")
    market = tag_to_market.get(tags[0], "idx")
    return MARKET_LABEL[market], tags[0]


def load_schema():
    """Return parsed schema JSON. Prefer local file, fall back to download."""
    if SCHEMA_PATH.exists():
        return json.loads(SCHEMA_PATH.read_text())
    url = SCHEMA_URL or os.environ.get(
        "SCHEMA_SOURCE_URL",
        "https://raw.githubusercontent.com/supertypeai/sectors_api_docs/main/schema.json",
    )
    print(f"Fetching schema from {url} ...")
    resp = urllib.request.urlopen(url, timeout=30)
    schema = json.loads(resp.read().decode())
    SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCHEMA_PATH.write_text(json.dumps(schema, indent=2))
    print(f"  {len(schema['paths'])} paths -> {SCHEMA_PATH}")
    return schema


def generate_table():
    schema = load_schema()
    intent_map = load_intent_map()

    # Build tag → market mapping
    tag_to_market = {}
    for group in schema["info"]["x-tagGroups"]:
        market_key = MARKET_BY_TAG_GROUP[group["name"]]
        for tag in group["tags"]:
            tag_to_market[tag] = market_key

    # Collect operations, skip phantoms
    kept = []
    for path, item in schema["paths"].items():
        op = item.get("get")
        if not op or has_phantom_path_param(path, op):
            continue
        market_label, tag = market_tag(op, tag_to_market)
        key = op["summary"]
        intent = intent_map.get(key, "")
        params = required_params(op)
        kept.append((market_label, tag, key, intent, params))

    # Sort by: market order, then tag order (within market), then key
    def sort_key(row):
        market_label, tag, key, _, _ = row
        return (MARKET_ORDER.get(market_label, 99), TAG_ORDER_IDX.get(tag, 99), key)

    kept.sort(key=sort_key)

    lines = [
        "| Market | User wants | Endpoint key | Required params |",
        "|---|---|---|---|",
    ]
    for market_label, tag, key, intent, params in kept:
        lines.append(f"| {market_label} | {intent} | `{key}` | {params} |")

    return "\n".join(lines) + "\n"


def replace_markers(text, table):
    """Replace content between markers. Leaves markers themselves intact."""
    pattern = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        re.DOTALL,
    )
    replacement = MARKER_START + "\n" + table + MARKER_END
    if not pattern.search(text):
        raise ValueError(f"Missing markers {MARKER_START!r} ... {MARKER_END!r}")
    return pattern.sub(replacement, text)


def update_file(path):
    skill_path = SRC_ROOT / path
    print(f"  {skill_path.relative_to(SRC_ROOT)} ...", end="")
    text = skill_path.read_text()
    table = generate_table()
    result = replace_markers(text, table)
    if result == text:
        print(" unchanged")
        return
    skill_path.write_text(result)
    print(" updated")


def main():
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    else:
        targets = ["SKILL.md"]

    print("Updating decision tables:")
    for t in targets:
        update_file(t)
    print("Done.")


if __name__ == "__main__":
    main()
