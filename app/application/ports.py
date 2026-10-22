from typing import Protocol

from app.domain.models import ConversationTurn


class LLMCLient(Protocol):
    def generate(self, prompt: str) -> str: ...


class ConversationRepository(Protocol):
    def save(self, turn: ConversationTurn) -> None: ...

    def list_all(self) -> list[ConversationTurn]: ...
