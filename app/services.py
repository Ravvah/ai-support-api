from uuid import uuid8

from app.schemas import AskRequest, AskResponse


class AnswerService:
    def answer(self, request: AskRequest) -> AskResponse:
        return AskResponse(answer="This is the response !", request_id=str(uuid8()))
