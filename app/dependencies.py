from typing import Annotated

from fastapi import Depends

from app.application.ports import ConversationRepository, LLMCLient
from app.application.services import AnswerService
from app.infrastructure.llm_fake import FakeLLM
from app.infrastructure.repository_sqlite import SQLiteConversationRepository, engine


def get_llm_client() -> LLMCLient:
    return FakeLLM()

def get_conversation_repository() -> ConversationRepository:
    return in_memory_conversation_repository


def get_answer_service(repository: Annotated[ConversationRepository, Depends(get_conversation_repository)]) -> AnswerService:
    return AnswerService(get_llm_client(), repository)


in_memory_conversation_repository = SQLiteConversationRepository(engine)


