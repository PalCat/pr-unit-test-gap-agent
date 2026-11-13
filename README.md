# pr-test-gap-agent

On every pull request: detect changed lines that lack test coverage, have an AI agent draft tests
(never touching `src/`), validate them, and open a review PR for a human to approve.

Status: Phase 1 (sample service + partial tests). See docs/rules.md for the pricing rules.

## Run locally
    pip install -r requirements.txt
    pytest --cov=src --cov-report=term-missing

## Coverage gate
`scripts/check_gap.sh [base-ref]` runs the tests and checks coverage of the lines changed vs. the base
branch (default `origin/main`). Threshold: `COVERAGE_THRESHOLD` env var (default 80). Exit 0 = covered,
1 = gap. CI calls this same script, so local and CI results match.
