from pydantic import BaseModel, Field


class ScamAnalysisRequest(BaseModel):
    text: str = Field(min_length=3, max_length=1000)


class ScamAnalysisResponse(BaseModel):
    risk_level: str
    score: int
    warnings: list[str]
    message: str