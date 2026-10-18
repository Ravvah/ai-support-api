from typing import Union
from uuid import uuid8

from app.llm import FakeLLM
from app.schemas import AskRequest, AskResponse


class AnswerService:

    def __init__(self, llm):
        self.llm = llm

    def answer(self, request: AskRequest) -> AskResponse:
        answer = self.llm.generate(request.question)
        return AskResponse(answer=answer, request_id=str(uuid8()))
