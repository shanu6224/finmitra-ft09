from decimal import Decimal

from pydantic import BaseModel, Field


class LoanEligibilityRequest(BaseModel):
    requested_amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    purpose: str = Field(min_length=3, max_length=255)


class LoanApplicationRequest(BaseModel):
    requested_amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    purpose: str = Field(min_length=3, max_length=255)
    client_application_id: str = Field(min_length=3, max_length=100)


class LoanEligibilityResponse(BaseModel):
    eligible: bool
    max_simulated_amount: Decimal
    reason: str


class LoanApplicationResponse(BaseModel):
    id: str
    purpose: str
    requested_amount: Decimal
    eligibility_status: str
    application_status: str

    model_config = {"from_attributes": True}
