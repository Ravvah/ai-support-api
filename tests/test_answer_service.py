from app.errors import LLMUnavailableError
from app.llm import FakeLLM
from app.schemas import AskRequest
from app.services import AnswerService

import pytest

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
def ask_request():
    return AskRequest(question="How a RAG is working ?")

@pytest.fixture
def fake_llm():
    return FakeLLM()

@pytest.fixture
def answer_service(fake_llm):
    return AnswerService(fake_llm)

def test_answer_service(answer_service, ask_request) -> None:
    response = answer_service.answer(request=ask_request)
    assert response.answer == f"FAKE : {ask_request.question}"


def test_failed_generation_when_llm_is_unavailable() -> None:
    request = AskRequest(question="How a RAG is working ?")
    failing_llm = FailingLLM()
    answer_service = AnswerService(failing_llm)
    with pytest.raises(LLMUnavailableError):
        answer_service.answer(request=request)


# @pytest.fixture
# def recording_llm():
#     return RecordingLLM()

def test_answer_send_question_to_llm() -> None:
    ask_request = AskRequest(question="How a RAG is working ?")
    recording_llm = RecordingLLM()
    answer_service = AnswerService(recording_llm)
    answer_service.answer(ask_request)

    assert ask_request.question in recording_llm.last_prompt

