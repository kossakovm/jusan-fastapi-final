from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_sum():
    response = client.get("/sum1n/7")
    assert response.status_code == 200
    assert response.json() == {"result": 28}

def test_fibonacci():
    response = client.get("/fibo?n=10")
    assert response.status_code == 200
    assert response.json() == {"result": 34}

def test_reverse():
    response = client.post("/reverse",headers={"string": "marlen"})
    assert response.status_code == 200
    assert response.json() == {"result": "nelram"}

def test_listPut():
    response = client.put("/list", json={"element":"Apple"})
    response = client.put("/list", json={"element":"Banana"})
    response = client.put("/list", json={"element":"Orange"})
    assert response.status_code == 200
    assert response.json() == {"result": ["Apple", "Banana", "Orange"]}

def test_listGet():
    response = client.get("/list")
    assert response.status_code == 200
    assert response.json() == {"result": ["Apple", "Banana", "Orange"]}

def test_calc():
    response_plus_oper = client.post("/calculator",json={"expr": "2,+,2"})
    assert response_plus_oper.status_code == 200
    assert response_plus_oper.json() == {"result": 4}