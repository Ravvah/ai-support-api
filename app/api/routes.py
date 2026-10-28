
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas import AskRequest, AskResponse, HistoryItemResponse
from app.application.ports import ConversationRepository
from app.application.services import AnswerService
from app.dependencies import get_answer_service, get_conversation_repository
from app.errors import QuestionTooLongError, EmptyQuestionError

router = APIRouter()


@router.get("/health")
def get_health() -> dict:
    return {"status": "ok"}


@router.post("/answer")
def answer_to_question(
    request: AskRequest, answer_service: Annotated[AnswerService, Depends(get_answer_service)]
) -> AskResponse:
    try:
        response = answer_service.answer(request)
    except QuestionTooLongError:
        raise HTTPException(
            status_code=422,
            detail="Question is too long"
        )
    except EmptyQuestionError:
        raise HTTPException(
            status_code=422,
            detail="Question is empty "
        )
    
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
