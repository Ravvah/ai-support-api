from fastapi.testclient import TestClient

from app.main import app
from app.schemas import AskRequest

client = TestClient(app)


def test_correct_answer() -> None:
    request = AskRequest(question="hello how are you?")
    response = client.post("/answer", json=request.model_dump())
    assert response.status_code == 200
    assert {"answer", "request_id"} == set(response.json().keys())
    assert len(response.json()["answer"]) > 0


def test_too_short_question_answer() -> None:
    response = client.post("/answer", json={"question": "he"})
    assert response.status_code == 422


def test_uncorrect_request_answer() -> None:
    response = client.post("/answer", json={})
    assert response.status_code == 422
