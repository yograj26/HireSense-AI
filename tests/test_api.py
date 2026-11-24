from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_api_is_running():
    response = client.get("/")
    assert response.status_code in [200, 404]


def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200