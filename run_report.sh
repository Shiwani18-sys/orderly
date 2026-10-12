#!/usr/bin/env bash
# Orderly — one-shot report runner.
# TODO(T4): complete the four marked steps, then run this script from the
# project root with Git Bash:  bash run_report.sh
!/usr/bin/env bash
set -euo pipefail


# Step 1 — detect a Python interpreter. Try python3, then python, then py.
# Hint: command -v prints the path of a command, or nothing if it is absent.
PY=""
# TODO(T4a): fill in detection so PY ends up with the first available of
# python3 / python / py. Never hard-code "python3" — fresh laptops differ.
if [ -z "$PY" ]; then
  echo "ERROR: no Python interpreter found" >&2
  exit 1
fi
echo "Using interpreter: $PY"

# Step 2 — build the database into out/orderly.db.
# TODO(T4b): create the out/ directory if needed, then run the CLI seed
# command using "$PY".

# Step 3 — generate the monthly revenue report into out/reports/.
# TODO(T4c): run the CLI report command with --db out/orderly.db
# --out out/reports

# Step 4 — archive the report directory.
# TODO(T4d): create out/reports.tar.gz containing the out/reports directory
# (use tar), then list the archive contents to prove it worked.

echo "run_report.sh finished"
