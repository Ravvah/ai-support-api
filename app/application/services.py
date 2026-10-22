from uuid import uuid8

from app.api.schemas import AskRequest, AskResponse
from app.application.ports import ConversationRepository, LLMCLient
from app.domain.models import ConversationTurn


class AnswerService:
    def __init__(self, llm: LLMCLient, repository: ConversationRepository):
        self.llm = llm
        self.repository = repository

    def answer(self, request: AskRequest) -> AskResponse:
        answer = self.llm.generate(request.question)
        request_id = str(uuid8())
        turn = ConversationTurn(id=request_id, question=request.question, answer=answer)
        self.repository.save(turn)
        return AskResponse(answer=answer, request_id=request_id)
