from fastapi import FastAPI

from app.schemas import AskRequest, AskResponse
from app.services import AnswerService

app = FastAPI()


@app.get("/health")
def get_health() -> dict:
    return {"status": "ok"}


@app.post("/answer")
def answer_to_question(request: AskRequest) -> AskResponse:
    service = AnswerService()
    response = service.answer(request)
    return response
