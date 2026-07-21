#!/usr/bin/env python3
"""Validate references/*.jsonl: every line is valid JSON, keys are unique
across each file, and required fields are present. Run in CI after
generate_references.py.
"""
import json
import sys
from pathlib import Path

REFERENCES_DIR = Path(__file__).resolve().parent.parent.parent / "references"
REQUIRED_FIELDS = {"key", "path", "method", "params"}


def validate_file(path):
    errors = []
    seen_keys = set()
    for i, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"{path.name}:{i}: invalid JSON ({e})")
            continue
        missing = REQUIRED_FIELDS - obj.keys()
        if missing:
            errors.append(f"{path.name}:{i}: missing fields {missing}")
        key = obj.get("key")
        if key in seen_keys:
            errors.append(f"{path.name}:{i}: duplicate key '{key}'")
        seen_keys.add(key)
    return errors


def main():
    files = sorted(REFERENCES_DIR.glob("*.jsonl"))
    if not files:
        print("No references/*.jsonl files found.", file=sys.stderr)
        return 1
    all_errors = []
    for f in files:
        all_errors.extend(validate_file(f))
    if all_errors:
        for e in all_errors:
            print(e, file=sys.stderr)
        print(f"\n{len(all_errors)} error(s) across {len(files)} file(s).", file=sys.stderr)
        return 1
    total_lines = sum(1 for f in files for l in f.read_text().splitlines() if l.strip())
    print(f"OK: {total_lines} endpoints across {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
