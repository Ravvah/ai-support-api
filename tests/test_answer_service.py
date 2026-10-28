import pytest

from app.api.schemas import AskRequest
from app.application.services import AnswerService
from app.errors import LLMUnavailableError, QuestionTooLongError, EmptyQuestionError
from app.infrastructure.llm_fake import FakeLLM
from app.infrastructure.repository_memory import InMemoryConversationRepository


class FailingLLM:
    def generate(self, prompt: str) -> str:
        raise LLMUnavailableError("Error to simulate failed generation !")


class RecordingLLM:
    def __init__(self):
        self.last_prompt = None

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return "RECORDED"


@pytest.fixture
def repository() -> InMemoryConversationRepository:
    return InMemoryConversationRepository()


@pytest.fixture
def ask_request():
    return AskRequest(question="How a RAG is working ?")


@pytest.fixture
def fake_llm():
    return FakeLLM()


@pytest.fixture
def answer_service(fake_llm, repository: InMemoryConversationRepository):
    return AnswerService(fake_llm, repository)


def test_answer_service(answer_service, ask_request) -> None:
    response = answer_service.answer(request=ask_request)
    assert response.answer == f"FAKE : {ask_request.question}"


def test_failed_generation_when_llm_is_unavailable() -> None:
    request = AskRequest(question="How a RAG is working ?")
    failing_llm = FailingLLM()
    repository = InMemoryConversationRepository()
    answer_service = AnswerService(failing_llm, repository)
    with pytest.raises(LLMUnavailableError):
        answer_service.answer(request=request)


# @pytest.fixture
# def recording_llm():
#     return RecordingLLM()


def test_answer_send_question_to_llm() -> None:
    ask_request = AskRequest(question="How a RAG is working ?")
    recording_llm = RecordingLLM()
    repository = InMemoryConversationRepository()
    answer_service = AnswerService(recording_llm, repository)
    answer_service.answer(ask_request)

    assert recording_llm.last_prompt is not None
    assert ask_request.question in recording_llm.last_prompt


def test_answer_saves_conversation_turn(fake_llm, ask_request) -> None:
    repository = InMemoryConversationRepository()
    answer_service = AnswerService(fake_llm, repository)

    answer_service.answer(ask_request)

    history = repository.list_all()

    assert len(history) == 1

    saved_turn = history[0]
    assert saved_turn.question == ask_request.question



def test_answer_rejects_question_longer_than_500_characters(answer_service: AnswerService) -> None:
    question = "a" * 501
    with pytest.raises(QuestionTooLongError):
        answer_service.answer(AskRequest(question=question))
    ...

def test_answer_rejects_whitespace_only_question(answer_service: AnswerService) -> None:
    question = "   "
    with pytest.raises(EmptyQuestionError):
        answer_service.answer(AskRequest(question=question))
