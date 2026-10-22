from fastapi.testclient import TestClient

from app.api.schemas import AskRequest, AskResponse
from app.dependencies import get_answer_service
from app.main import app

client = TestClient(app)


class StubAnswerService:
    def answer(self, request: AskRequest) -> AskResponse:
        return AskResponse(answer="Test Response", request_id="test-response-id")


def test_correct_answer() -> None:
    app.dependency_overrides[get_answer_service] = lambda: StubAnswerService()
    request = AskRequest(question="hello how are you?")
    response = client.post("/answer", json=request.model_dump())
    assert response.status_code == 200
    assert {"answer", "request_id"} == set(response.json().keys())
    assert response.json() == {
        "answer": "Test Response",
        "request_id": "test-response-id",
    }

    app.dependency_overrides.clear()


def test_too_short_question_answer() -> None:
    response = client.post("/answer", json={"question": "he"})
    assert response.status_code == 422


def test_uncorrect_request_answer() -> None:
    response = client.post("/answer", json={})
    assert response.status_code == 422
