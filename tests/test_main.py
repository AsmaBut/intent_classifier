from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# 1️ Health Check

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API is running"}

# 2️ Single Query Classification

def test_classify_single():
    response = client.post("/api/classify", json={"text": "Send an email to John"})
    assert response.status_code == 200
    data = response.json()
    assert "intent" in data
    assert "confidence" in data
    assert data["text"] == "Send an email to John"


# 3️ Batch Classification

def test_classify_batch():
    texts = ["Send an email to John", "Schedule a meeting"]
    response = client.post("/api/classify/batch", json={"texts": texts})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for item, text in zip(data, texts):
        assert item["text"] == text
        assert "intent" in item
        assert "confidence" in item


# 4 Model Info (Basic Auth)

def test_model_info():
    response = client.get("/api/model/info", auth=("admin", "admin123"))
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "classes" in data
    assert "num_classes" in data
