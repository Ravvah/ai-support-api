from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., description="user question", min_length=3)


class AskResponse(BaseModel):
    answer: str = Field(..., description="model response")
    request_id: str = Field(..., description="request id")
