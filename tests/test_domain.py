from app.domain.models import ConversationTurn


def test_create_conversation_turn() -> None:
    turn = ConversationTurn(
        id="123",
        question="How a RAG is working ?",
        answer="A RAG is a prompt injection automation for context providance",
    )

    assert turn.question == "How a RAG is working ?"
