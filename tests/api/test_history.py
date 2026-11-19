import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_conversation_repository
from app.infrastructure.repository_memory import InMemoryConversationRepository
from app.main import app

client = TestClient(app)

test_repository = InMemoryConversationRepository()

def override_get_conversation_repository() -> InMemoryConversationRepository:
    return test_repository

app.dependency_overrides[get_conversation_repository] = (
    override_get_conversation_repository
    )

@pytest.fixture(autouse=True)
def clean_repository() -> None:
    test_repository.clear()


def test_history_contains_turn_after_answer() -> None:
    answer_response = client.post(
        "/answer", json={"question": "How a RAG is working ?"}
    )

    assert answer_response.status_code == 200

    history_response = client.get("/history")

    assert history_response.status_code == 200
    assert len(history_response.json()) == 1
    assert history_response.json()[0]["question"] == "How a RAG is working ?"


# def test_history_is_empty_initially() -> None:
#     response = client.get("/history")

#     assert response.status_code == 200
#     assert response.json() == []
