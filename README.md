# SecureSOC

**AI-Powered Local SOC & Agent Security Lab**

SecureSOC is a security operations platform that runs entirely on one workstation. It combines deterministic threat detection with a local LLM agent that investigates incidents — and treats that agent as an **untrusted component**. The agent can reason and propose actions. It cannot authorise them: every tool request goes through an independent policy engine, high-impact actions need human approval, and everything is written to a tamper-evident audit log.

> **Status: Phase 1 — Foundation.** The repository skeleton, API, database, migrations and dashboard shell are in place. Detection, incidents and the agent arrive in later phases (see [Roadmap](#roadmap)).

```text
events → ingestion → normalisation → deterministic detection → correlation → alert → incident
                                                                                       │
                     audit log ◄── executor ◄── [human approval] ◄── policy engine ◄── AI agent → tool request
```

| Principle | Meaning |
|---|---|
| LLM = orchestration | Interprets evidence, selects tools, writes reports |
| Policy engine = authorisation | Deterministic `ALLOW` / `DENY` / `REQUIRE_APPROVAL`, deny by default |
| Human = control | Approves sensitive actions; the agent has no way to approve |
| Audit = traceability | Append-only, written by code, never by the model |
| Cost = €0 | No paid API, cloud, hosting or SaaS. Everything is local. |

## Quick start

Requirements: Docker (Desktop or Engine), Git. Optional for development: Python 3.12 + [uv](https://docs.astral.sh/uv/), Node.js ≥ 22.

```bash
cp .env.example .env          # PowerShell: Copy-Item .env.example .env
# edit .env and set POSTGRES_PASSWORD
docker compose up -d
```

Open <http://localhost:3000>. The status pill in the top bar should read **API ready**.

| Service | URL | Notes |
|---|---|---|
| Dashboard | http://localhost:3000 | nginx serving the React build, proxies `/api` |
| API | http://localhost:8000/api/v1/health | FastAPI |
| PostgreSQL | localhost:5433 | Host port 5433 avoids clashing with a local install |

All ports are bound to `127.0.0.1` only.

## Development

```bash
docker compose up -d db                      # database only

cd apps/api
uv sync                                      # create .venv from uv.lock
uv run alembic upgrade head
uv run uvicorn securesoc.main:app --reload   # http://localhost:8000/api/docs

cd apps/web
npm install
npm run dev                                  # http://localhost:3000 (proxies /api to :8000)
```

### Checks (same as CI)

```bash
# API
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
# Web
npm run lint && npm run typecheck && npm test && npm run build
```

If the database is not running, integration tests are skipped locally. In CI they are mandatory.

## Repository layout

```text
apps/api     FastAPI backend (single Python package `securesoc`, modules enforced by an import-boundary test)
apps/web     React + TypeScript + Vite + Tailwind dashboard
docs/        planning, ADRs, architecture and security documentation
scripts/     helper scripts (e.g. read-only system report for Windows)
```

Later phases add `rules/`, `policies/`, `datasets/`, `redteam/` and `labs/`.

## Security

- Secrets live only in `.env` (git-ignored); see `.env.example`.
- Containers run as non-root with read-only filesystems, `cap_drop: ALL` and `no-new-privileges`.
- The dashboard sends a strict Content-Security-Policy, and rendering raw HTML is blocked by lint.
- Readiness checks never return connection errors to clients.
- Offensive lab tooling targets **only the project's own isolated VMs**.

See [SECURITY.md](SECURITY.md).

## Roadmap

| Phase | Scope | Status |
|---|---|---|
| 0 | Design, hardware analysis, model choice | ✅ |
| 1 | Foundation: repo, Docker, PostgreSQL, FastAPI, React, migrations, CI | ✅ |
| 2 | Ingestion: canonical event schema, Linux auth / UFW parsers | ⏳ |
| 3 | Detection: Sigma-subset engine, SSH brute force, port scan, login after failures | |
| 4 | Incidents: correlation, timeline, MITRE ATT&CK mapping | |
| 5 | Dashboard: incidents, evidence, alert explanations | |
| 6 | AI: Ollama provider, investigation agent, read-only tools | |
| 7 | Security layer: tool registry, policy engine, audit chain, RBAC | |
| 8 | Human approval workflow | |
| 9 | Red team: prompt injection, tool abuse, regression benchmark | |
| 10 | Lab demo, evaluation, documentation | |

The full plan is in [`docs/planning/fase-0-planificacion.md`](docs/planning/fase-0-planificacion.md) (Spanish) and the decisions are in [`docs/adr/`](docs/adr/README.md).

## License

[Apache-2.0](LICENSE)
