from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "welcome to my api"
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users/", json={"name":"test","email":"test1@gmail.com", "password":"test123"})
    print(res.json())
    assert res.status_code == 201