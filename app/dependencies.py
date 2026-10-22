from app.application.ports import ConversationRepository, LLMCLient
from app.application.services import AnswerService
from app.infrastructure.llm_fake import FakeLLM
from app.infrastructure.repository_memory import InMemoryConversationRepository


def get_llm_client() -> LLMCLient:
    return FakeLLM()


def get_answer_service() -> AnswerService:
    return AnswerService(get_llm_client(), get_conversation_repository())


in_memory_conversation_repository = InMemoryConversationRepository()


def get_conversation_repository() -> ConversationRepository:
    return in_memory_conversation_repository
