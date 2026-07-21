#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "==> Generating references …"
python3 scripts/pipeline/generate_references.py

echo "==> Updating decision tables …"
python3 scripts/pipeline/update_skill_md.py

echo "==> Validating …"
python3 scripts/pipeline/validate_references.py

echo "Done."
