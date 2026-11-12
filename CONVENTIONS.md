# Test conventions (read by the agent)

- Framework: pytest. Tests live under `tests/unit/`, one file per source module: `test_<module>.py`.
- Names: `test_<function>_<scenario>_<expected>`.
- Prefer `pytest.mark.parametrize` for input/output tables.
- Assert on behavior defined in `docs/rules.md`, not on how the code happens to work.
- If code and rules disagree, do NOT write a passing test around it. Report a suspected bug.
- No real network, no real clock: pass `today=` explicitly for date-dependent logic.
- Never edit anything under `src/`.
