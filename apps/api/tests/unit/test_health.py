from fastapi.testclient import TestClient

from securesoc import __version__


def test_health_returns_ok_and_version(client: TestClient) -> None:
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "version": __version__}


def test_ready_returns_503_when_database_is_down(client_without_db: TestClient) -> None:
    r = client_without_db.get("/api/v1/health/ready")
    assert r.status_code == 503
    assert r.json() == {"status": "unavailable", "checks": {"database": "error"}}


def test_ready_failure_does_not_leak_connection_details(client_without_db: TestClient) -> None:
    body = client_without_db.get("/api/v1/health/ready").text.lower()
    for leak in ("127.0.0.1", "password", "psycopg", "traceback", "connection"):
        assert leak not in body
