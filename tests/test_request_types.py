from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app,raise_server_exceptions=False)

def test_json_array_rejected():
    response=client.post("/api/run",json=[])
    assert response.status_code==422 and response.json()["error"]=="PAYLOAD"

def test_module_array_rejected():
    assert client.post("/api/1",json=[]).status_code==422

def test_review_unhashable_decision_rejected():
    response=client.post("/api/review",json={"id":"x","revision":0,"decision":[]})
    assert response.status_code==422 and response.json()["error"]=="REVIEW"

def test_review_bool_revision_rejected():
    assert client.post("/api/review",json={"id":"x","revision":True,"decision":"退回"}).status_code==422

def test_json_null_rejected():
    assert client.post("/api/run",content="null",headers={"Content-Type":"application/json"}).status_code==422
