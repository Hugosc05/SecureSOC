# SecureSOC

**SOC local con IA y laboratorio de seguridad de agentes**

[![CI](https://github.com/Hugosc05/SecureSOC/actions/workflows/ci.yml/badge.svg)](https://github.com/Hugosc05/SecureSOC/actions/workflows/ci.yml)
![Coste](https://img.shields.io/badge/coste-0%E2%82%AC-2ea44f)
![Licencia](https://img.shields.io/badge/licencia-Apache--2.0-blue)

SecureSOC es una plataforma de operaciones de seguridad (SOC) que se ejecuta entera en un solo ordenador. Combina detección de amenazas determinista con un agente LLM local que investiga incidentes, y trata a ese agente como un **componente no confiable**. El agente puede razonar y proponer acciones, pero no puede autorizarlas:

- toda petición de herramienta pasa por un motor de políticas independiente;
- las acciones de alto impacto necesitan aprobación humana;
- todo queda registrado en un log de auditoría a prueba de manipulaciones.

> **Estado: Fase 1 — Foundation.** Ya están el esqueleto del repositorio, la API, la base de datos, las migraciones y la estructura del dashboard. La detección, los incidentes y el agente llegan en las siguientes fases (ver [Roadmap](#roadmap)).

```text
eventos → ingesta → normalización → detección determinista → correlación → alerta → incidente
                                                                                    │
                 audit log ◄── ejecutor ◄── [aprobación humana] ◄── policy engine ◄── agente IA → petición de tool
```

| Principio | Significado |
|---|---|
| LLM = orquestación | Interpreta evidencias, elige herramientas y redacta informes |
| Policy engine = autorización | `ALLOW` / `DENY` / `REQUIRE_APPROVAL` deterministas; por defecto, denegar |
| Humano = control | Aprueba las acciones sensibles; el agente no tiene ninguna forma de aprobar |
| Auditoría = trazabilidad | Solo se añade (append-only), la escribe el código y nunca el modelo |
| Coste = 0 € | Sin APIs de pago, cloud, hosting ni SaaS. Todo es local. |

## Puesta en marcha

Requisitos: Docker (Desktop o Engine) y Git. Para desarrollar, además: Python 3.12 + [uv](https://docs.astral.sh/uv/) y Node.js ≥ 22.

```powershell
Copy-Item .env.example .env    # Linux/macOS: cp .env.example .env
# edita .env y pon una contraseña en POSTGRES_PASSWORD
docker compose up -d
```

Abre <http://localhost:3000>. El indicador de la barra superior debería poner **API ready**.

| Servicio | URL | Notas |
|---|---|---|
| Dashboard | http://localhost:3000 | nginx sirve el build de React y reenvía `/api` a la API |
| API | http://localhost:8000/api/v1/health | FastAPI |
| PostgreSQL | localhost:5433 | Puerto 5433 para no chocar con una instalación local en el 5432 |

Todos los puertos escuchan solo en `127.0.0.1`: nada es accesible desde tu red.

## Desarrollo

```bash
docker compose up -d db                      # solo la base de datos

cd apps/api
uv sync                                      # crea .venv a partir de uv.lock
uv run alembic upgrade head
uv run uvicorn securesoc.main:app --reload   # http://localhost:8000/api/docs

cd apps/web
npm install
npm run dev                                  # http://localhost:3000 (reenvía /api al :8000)
```

### Comprobaciones (las mismas que el CI)

```bash
# API
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
# Web
npm run lint && npm run typecheck && npm test && npm run build
```

Si la base de datos no está arrancada, los tests de integración se saltan en local. En el CI son obligatorios.

## Estructura del repositorio

```text
apps/api     Backend FastAPI (un único paquete Python `securesoc`; un test vigila las fronteras entre módulos)
apps/web     Dashboard en React + TypeScript + Vite + Tailwind
docs/        planificación, decisiones de arquitectura (ADR) y documentación de seguridad
scripts/     scripts de apoyo (p. ej. informe de solo lectura del sistema Windows)
```

En las siguientes fases se añaden `rules/`, `policies/`, `datasets/`, `redteam/` y `labs/`.

## Seguridad

- Los secretos solo viven en `.env`, que está en `.gitignore`. La plantilla es `.env.example`.
- Los contenedores no corren como root: sistema de archivos de solo lectura, `cap_drop: ALL` y `no-new-privileges`.
- El dashboard envía una Content-Security-Policy estricta, y el lint prohíbe renderizar HTML en bruto.
- Las comprobaciones de salud nunca devuelven errores de conexión al cliente.
- Las herramientas ofensivas del laboratorio atacan **solo a las propias VMs aisladas del proyecto**.

Más detalles en [SECURITY.md](SECURITY.md).

## Roadmap

| Fase | Alcance | Estado |
|---|---|---|
| 0 | Diseño, análisis de hardware y elección del modelo | ✅ |
| 1 | Foundation: repositorio, Docker, PostgreSQL, FastAPI, React, migraciones y CI | ✅ |
| 2 | Ingesta: esquema común de eventos y parsers de Linux auth / UFW | ⏳ |
| 3 | Detección: motor con un subconjunto de Sigma (fuerza bruta SSH, escaneo de puertos, login tras fallos) | |
| 4 | Incidentes: correlación, timeline y mapeo a MITRE ATT&CK | |
| 5 | Dashboard: incidentes, evidencias y explicación de las alertas | |
| 6 | IA: proveedor Ollama, agente investigador y herramientas de solo lectura | |
| 7 | Capa de seguridad: registro de herramientas, policy engine, cadena de auditoría y RBAC | |
| 8 | Flujo de aprobación humana | |
| 9 | Red team: prompt injection, abuso de herramientas y benchmark de regresión | |
| 10 | Demo del laboratorio, evaluación y documentación | |

El plan completo está en [`docs/planning/fase-0-planificacion.md`](docs/planning/fase-0-planificacion.md) y las decisiones en [`docs/adr/`](docs/adr/README.md).

## Licencia

[Apache-2.0](LICENSE)
