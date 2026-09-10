from pydantic import BaseModel, Field


class AssistantIntentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)
    language: str = Field(default="en", pattern="^(en|ta)$")


class AssistantIntentResponse(BaseModel):
    intent: str
    amount: float | None = None
    requires_confirmation: bool = True
    message: str
