from fastapi.testclient import TestClient

from fastapi_app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_status():
    response = client.get("/api/v1/status/")
    assert response.status_code == 200


def test_ai_status():
    response = client.get("/api/v1/ai/status")
    assert response.status_code == 200
