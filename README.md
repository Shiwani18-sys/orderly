# Orderly

Orderly is a small command-line tool that builds a SQLite database of retail
orders and produces sales reports (monthly revenue, top customers, category
breakdowns).

complete the "Setup" section below — a new teammate must be
     able to get from zero to a passing test run using only this README
## Setup

_TODO(T7a): document how to set up the project on a fresh machine: required
tools, installing test dependencies offline from `vendor/`, and how to run
`verify_env.py`._

## Usage

 

_TODO(T7b): usage examples go here._
/*document the two CLI commands below (seed, report) with one
     copy-pasteable example each, including what output is produced and
     where*/


> **Running the CLI:** the package lives under `src/`, so when you run CLI
> commands directly from Git Bash, prefix them with `PYTHONPATH=src`, e.g.
> `PYTHONPATH=src python -m orderly.cli seed --db out/orderly.db`.

## Project layout

| Path | Purpose |
|---|---|
| `src/orderly/` | application package (`db`, `reports`, `cli`) |
| `data/seed.sql` | deterministic seed data — do not edit |
| `tests/` | pytest suite with expected values baked in |
| `vendor/` | vendored wheels for offline installs |
| `verify_env.py` | environment self-check |
| `run_report.sh` | one-shot report runner (Task T4) |

## Troubleshooting

<!-- TODO(T7c): add at least two troubleshooting entries covering problems
     you actually hit during this exercise (symptom + cause + fix). -->

_TODO(T7c): troubleshooting entries go here._
