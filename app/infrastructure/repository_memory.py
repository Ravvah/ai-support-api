
from app.domain.models import ConversationTurn


class InMemoryConversationRepository:
    def __init__(self):
        self._items: list[ConversationTurn] = []

    def save(self, turn: ConversationTurn) -> None:
        self._items.append(turn)

    def list_all(self) -> list[ConversationTurn]:
        return self._items.copy()

    def clear(self) -> None:
        return self._items.clear()
