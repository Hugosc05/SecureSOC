"""Application factory.

Run locally:  uv run uvicorn securesoc.main:app --reload
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from securesoc import __version__
from securesoc.api.v1 import router as v1_router
from securesoc.config import Settings, get_settings


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    _configure_logging(settings.log_level)

    app = FastAPI(
        title="SecureSOC API",
        version=__version__,
        # Interactive docs are handy in development but expose the full surface;
        # they are switched off in production.
        docs_url="/api/docs" if settings.docs_enabled else None,
        redoc_url=None,
        openapi_url="/api/openapi.json" if settings.docs_enabled else None,
    )
    app.include_router(v1_router)
    return app


app = create_app()
