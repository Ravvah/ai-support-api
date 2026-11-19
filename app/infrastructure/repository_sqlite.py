from datetime import UTC

from sqlalchemy import (
    Column,
    DateTime,
    Engine,
    MetaData,
    String,
    Table,
    create_engine,
    select,
)

from app.domain.models import ConversationTurn

engine = create_engine("sqlite:///./conversations.db")
metadata = MetaData()

conversations_table = Table(
    "conversations",
    metadata,
    Column("id", String, primary_key=True),
    Column("question", String, nullable=False),
    Column("answer", String, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

metadata.create_all(engine)

class SQLiteConversationRepository:

    def __init__(self, engine: Engine):
        self.engine = engine
    
    def save(self, turn: ConversationTurn) -> None:
        statement = conversations_table.insert().values(
            id=turn.id,
            question=turn.question,
            answer=turn.answer,
            created_at=turn.created_at
        )

        with self.engine.begin() as connection:
            connection.execute(statement)
    
    def list_all(self) -> list[ConversationTurn]:
        statement = select(conversations_table)
        with self.engine.begin() as connection:
            result = connection.execute(statement)
            rows = result.fetchall()
        
        return [
            ConversationTurn(
                id=row.id,
                question=row.question,
                answer=row.answer,
                created_at=row.created_at.replace(tzinfo=UTC)
        )
            for row in rows
        ]

