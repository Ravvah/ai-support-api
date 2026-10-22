from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ConversationTurn:
    id: str
    question: str
    answer: str
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
