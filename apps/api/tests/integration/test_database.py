from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, text

pytestmark = pytest.mark.integration

ALEMBIC_INI = Path(__file__).resolve().parents[2] / "alembic.ini"


def test_ready_returns_200_with_real_database(db_engine: Engine, client: TestClient) -> None:
    r = client.get("/api/v1/health/ready")
    assert r.status_code == 200
    assert r.json() == {"status": "ready", "checks": {"database": "ok"}}


def test_migrations_upgrade_and_downgrade_cleanly(db_engine: Engine) -> None:
    cfg = Config(str(ALEMBIC_INI))
    with db_engine.begin() as conn:
        cfg.attributes["connection"] = conn
        command.upgrade(cfg, "head")
        version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
        assert version == "0001"
        command.downgrade(cfg, "base")
        command.upgrade(cfg, "head")
