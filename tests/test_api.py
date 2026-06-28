from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Complejidad App API"


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analysis_stats():
    response = client.post("/api/v1/analysis/stats", json={"values": [4, 8, 15, 16, 23, 42]})
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 6
    assert data["min"] == 4
    assert data["max"] == 42
    assert "histogram" in data


def test_analysis_stats_empty_values():
    response = client.post("/api/v1/analysis/stats", json={"values": []})
    assert response.status_code == 422
