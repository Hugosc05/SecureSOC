from fastapi.testclient import TestClient
from pydantic import SecretStr

from securesoc.config import Environment, Settings
from securesoc.main import create_app


def test_password_is_never_rendered() -> None:
    s = Settings(db_password=SecretStr("super-secret-value"))
    assert s.db_password.get_secret_value() == "super-secret-value"  # really set
    assert "super-secret-value" not in repr(s)
    assert "super-secret-value" not in str(s.database_url)  # URL masks the password


def test_password_is_used_for_connections() -> None:
    s = Settings(db_password=SecretStr("pw"))
    assert s.database_url.password == "pw"


def test_postgres_env_names_are_shared_with_container(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("POSTGRES_USER", "alice")
    monkeypatch.setenv("POSTGRES_DB", "socdb")
    s = Settings()
    assert (s.db_user, s.db_name) == ("alice", "socdb")


def test_docs_are_disabled_in_production() -> None:
    app = create_app(Settings(environment=Environment.PRODUCTION))
    with TestClient(app) as c:
        assert c.get("/api/docs").status_code == 404
        assert c.get("/api/openapi.json").status_code == 404


def test_docs_are_enabled_in_development() -> None:
    app = create_app(Settings(environment=Environment.DEVELOPMENT))
    with TestClient(app) as c:
        assert c.get("/api/openapi.json").status_code == 200
