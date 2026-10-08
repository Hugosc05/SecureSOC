# Architecture Decision Records

Each decision records what was chosen, the alternative that was considered, and why. The full reasoning (in Spanish) is in [`../planning/fase-0-planificacion.md`](../planning/fase-0-planificacion.md).

| ID | Decision | Status | Alternative considered | Rationale |
|---|---|---|---|---|
| D-01 | Ollama runs natively on the host, outside Docker | Accepted | Ollama in Docker with GPU passthrough | Direct GPU access, no extra layer on Windows |
| D-02 | Default model `qwen3:8b` (Q4_K_M), light mode `qwen3:4b`; final choice by benchmark in Phase 6 | Accepted (provisional) | `qwen3.5:9b` | Fits fully in 8 GB VRAM with 8K context |
| D-03 | Docker Desktop (or Docker Engine in WSL2) | Accepted | Podman | Already installed; standard |
| D-04 | Single Python package with import-boundary tests | Accepted | Separate `packages/*` distributions | One deployable service; boundaries enforced by test |
| D-05 | Own detection engine loading a Sigma subset, including correlation rules | Accepted | pySigma + backend | pySigma converts rules to queries; it does not evaluate events |
| D-06 | Own policy engine with YAML policies, deny by default | Accepted | OPA / Rego | Testable, understandable, no extra service; OPA possible later as an adapter |
| D-07 | No agent framework; own loop over the Ollama REST API | Accepted | LangChain / LangGraph | The security mechanics must be explicit and auditable |
| D-08 | No RAG / pgvector in the MVP | Accepted | pgvector from day one | No measured need yet |
| D-09 | Synchronous SQLAlchemy 2.0 + psycopg 3 | Accepted | Async SQLAlchemy | Simpler; low load |
| D-10 | High-risk actions are simulated in the MVP | Accepted | Real nftables on the lab VM | Safety first; real response comes post-MVP |
| D-11 | Stdlib-only log shipper on the lab VM | Accepted | rsyslog forwarding, Vector, Fluent Bit | Zero dependencies on the victim host |
| D-12 | uv for Python environments and lockfile | Accepted | pip + venv | Reproducible lockfile, fast |
| D-13 | Documentation (README, docs) in Spanish; code, identifiers and commit messages in English | Accepted (revised 2026-10-08) | All English | The author is a Spanish speaker and the project doubles as a TFG; code stays in English by convention |
| D-14 | Apache-2.0 license | Accepted | MIT | Includes an explicit patent grant |
| D-15 | PostgreSQL exposed on host port 5433 | Accepted | 5432 | Avoids clashing with existing local installs |
| D-16 | Frontend served by `nginx-unprivileged`; `/api` reverse-proxied | Accepted | Separate origins + CORS | Same origin, strict CSP, non-root |
