
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.schemas import AskRequest, AskResponse, HistoryItemResponse
from app.application.ports import ConversationRepository
from app.application.services import AnswerService
from app.dependencies import get_answer_service, get_conversation_repository

router = APIRouter()


@router.get("/health")
def get_health() -> dict:
    return {"status": "ok"}


@router.post("/answer")
def answer_to_question(
    request: AskRequest, answer_service: Annotated[AnswerService, Depends(get_answer_service)]
) -> AskResponse:
    response = answer_service.answer(request)
    return response


@router.get("/history")
def get_history(
    repository: Annotated[ConversationRepository, Depends(get_conversation_repository)],
) -> list[HistoryItemResponse]:

    history = repository.list_all()

    return [
        HistoryItemResponse(
            id=turn.id,
            question=turn.question,
            answer=turn.answer,
            created_at=turn.created_at,
        )
        for turn in history
    ]
