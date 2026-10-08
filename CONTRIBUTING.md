# Contributing

## Workflow

1. Create a branch from `main`.
2. Keep changes small and focused, with tests in the same change.
3. Run the checks locally (see README → *Checks*) before opening a pull request.
4. Update `CHANGELOG.md` under **Unreleased**.

## Rules

- **Tests first-class:** new detection rules need positive, negative and boundary fixtures. New tools need policy tests.
- **Dependencies:** explain why a new dependency is needed, why existing tools are not enough, and confirm it is free and open source.
- **Architecture changes** need a new ADR in `docs/adr/`.
- **Never** commit secrets, real logs from third parties, or model weights.
- **Never** render untrusted data (logs, LLM output) as HTML.

## Commit messages

Use the imperative mood with a short scope, e.g. `api: add readiness check` or `web: add health indicator`.
