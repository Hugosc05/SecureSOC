"""Shared fixtures.

Integration tests need a real PostgreSQL. When it is unreachable they are
skipped locally, but fail when SECURESOC_REQUIRE_DB=1 (set in CI) so a broken
database can never turn into a silent green build.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine

from securesoc.config import Environment, Settings, get_settings
from securesoc.db.session import get_engine, ping_database
from securesoc.main import create_app

UNREACHABLE_DB = {"db_host": "127.0.0.1", "db_port": 1, "db_connect_timeout_s": 1}


@pytest.fixture
def settings() -> Settings:
    return Settings(environment=Environment.TEST)


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    app = create_app(settings)
    with TestClient(app) as c:
        yield c


@pytest.fixture
def client_without_db(settings: Settings) -> Iterator[TestClient]:
    """App whose database is unreachable (port 1), to test failure paths."""
    broken = settings.model_copy(update=UNREACHABLE_DB)
    engine = create_engine(
        broken.database_url, connect_args={"connect_timeout": broken.db_connect_timeout_s}
    )
    app = create_app(broken)
    app.dependency_overrides[get_engine] = lambda: engine
    with TestClient(app) as c:
        yield c
    engine.dispose()


@pytest.fixture(scope="session")
def db_engine() -> Iterator[Engine]:
    engine = create_engine(get_settings().database_url)
    try:
        ping_database(engine)
    except Exception as exc:
        engine.dispose()
        if os.environ.get("SECURESOC_REQUIRE_DB") == "1":
            pytest.fail(f"PostgreSQL required but unreachable: {type(exc).__name__}")
        pytest.skip("PostgreSQL not reachable; start it with `docker compose up -d db`")
    yield engine
    engine.dispose()
