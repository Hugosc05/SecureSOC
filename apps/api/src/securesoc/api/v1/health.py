"""Liveness and readiness probes.

- /health        -> the process is up (no dependencies touched).
- /health/ready  -> the process can serve traffic (database reachable).

Readiness never returns exception text to the client: connection errors can
contain hostnames or usernames. Details go to the server log only.
"""

from __future__ import annotations

import logging
from enum import StrEnum
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from sqlalchemy import Engine

from securesoc import __version__
from securesoc.db.session import get_engine, ping_database

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


class CheckStatus(StrEnum):
    OK = "ok"
    ERROR = "error"


class HealthResponse(BaseModel):
    status: str
    version: str


class ReadinessResponse(BaseModel):
    status: str
    checks: dict[str, CheckStatus]


@router.get("", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    responses={503: {"model": ReadinessResponse}},
)
def ready(
    response: Response,
    engine: Annotated[Engine, Depends(get_engine)],
) -> ReadinessResponse:
    checks: dict[str, CheckStatus] = {}

    try:
        ping_database(engine)
        checks["database"] = CheckStatus.OK
    except Exception:  # any driver/network error means "not ready"
        logger.exception("readiness: database check failed")
        checks["database"] = CheckStatus.ERROR

    ok = all(c is CheckStatus.OK for c in checks.values())
    if not ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadinessResponse(status="ready" if ok else "unavailable", checks=checks)
