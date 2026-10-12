

!/usr/bin/env bash
set -euo pipefail



PY=""

if [ -z "$PY" ]; then
  echo "ERROR: no Python interpreter found" >&2
  exit 1
fi
echo "Using interpreter: $PY"



echo "run_report.sh finished"
