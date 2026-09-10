from decimal import Decimal

from pydantic import BaseModel


class FinancialSummaryResponse(BaseModel):
    balance: Decimal
    currency: str
    total_savings: Decimal
    total_transactions: int
    loan_applications: int
    pending_loans: int