from sqlalchemy import create_engine

from app.domain.models import ConversationTurn
from app.infrastructure.repository_sqlite import SQLiteConversationRepository, metadata


def test_save_and_list_all() -> None:
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)

    repository = SQLiteConversationRepository(engine)

    turn = ConversationTurn(
        id="123",
        question="How a RAG is working ?",
        answer = "RAG is a prompt injection automation"
    )

    repository.save(turn)

    saved_turns = repository.list_all()

    assert len(saved_turns) == 1
    assert saved_turns[0] == turn