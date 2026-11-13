#!/usr/bin/env bash
# Deterministic coverage-gap check: are the lines changed vs. a base branch covered by tests?
#
# Usage:  scripts/check_gap.sh [base-ref]        (default: origin/main)
# Env:    COVERAGE_THRESHOLD   percent of changed lines that must be covered (default: 80)
# Exit:   0 = covered, 1 = gap found, other = tooling error
# Output: coverage.xml, diff-cover.md; and `gap=true|false` appended to $GITHUB_OUTPUT when set.
set -uo pipefail

BASE="${1:-origin/main}"
THRESHOLD="${COVERAGE_THRESHOLD:-80}"

pytest --cov=src --cov-report=xml -q || { echo "Tests failed; fix them before checking coverage."; exit 2; }

diff-cover coverage.xml \
  --compare-branch="$BASE" \
  --fail-under="$THRESHOLD" \
  --format markdown:diff-cover.md
code=$?

if [ "$code" -eq 0 ]; then gap=false; elif [ "$code" -eq 1 ]; then gap=true; else gap=error; fi
echo "gap=$gap (threshold ${THRESHOLD}%, base $BASE)"
[ -n "${GITHUB_OUTPUT:-}" ] && echo "gap=$gap" >> "$GITHUB_OUTPUT"
exit "$code"
