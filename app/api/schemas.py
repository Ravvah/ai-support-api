from datetime import datetime

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., description="user question", min_length=3)


class AskResponse(BaseModel):
    answer: str = Field(..., description="model response")
    request_id: str = Field(..., description="request id")


class HistoryItemResponse(BaseModel):
    id: str = Field(..., description="id of the turn")
    question: str = Field(..., description="user question of the turn")
    answer: str = Field(..., description="model response of the turn")
    created_at: datetime = Field(..., description="Creation time of the turn")
