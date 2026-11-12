# pr-test-gap-agent

On every pull request: detect changed lines that lack test coverage, have an AI agent draft tests
(never touching `src/`), validate them, and open a review PR for a human to approve.

Status: Phase 1 (sample service + partial tests). See docs/rules.md for the pricing rules.

## Run locally
    pip install -r requirements.txt
    pytest --cov=src --cov-report=term-missing
