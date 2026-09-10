from pydantic import BaseModel


class InsuranceResponse(BaseModel):
    id: int
    category: str
    title: str
    description: str
    eligibility: str
    documents_required: str

    model_config = {"from_attributes": True}
