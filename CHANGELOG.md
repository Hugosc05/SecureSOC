# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-08

### Added
- Phase 0 planning document and Architecture Decision Records D-01 to D-14.
- FastAPI backend skeleton with typed settings, `/api/v1/health` and `/api/v1/health/ready`.
- SQLAlchemy 2.0 + Alembic with a baseline migration.
- Architecture test enforcing import boundaries between modules (for example, `policy` may never import `agent` or `llm`).
- React + TypeScript + Vite + Tailwind dashboard shell with a live API health indicator.
- Docker Compose stack (PostgreSQL, one-shot migrations, API, nginx) bound to `127.0.0.1`, running hardened non-root containers.
- GitHub Actions CI: ruff, mypy, pytest with PostgreSQL, ESLint, tsc, Vitest, build, dependency audits, secret scanning, image builds.
- Read-only Windows system report script.
