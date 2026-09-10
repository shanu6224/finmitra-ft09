from decimal import Decimal

from pydantic import BaseModel, Field


class SavingsRequest(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    client_transaction_id: str = Field(min_length=1, max_length=80)


class SyncTransaction(BaseModel):
    client_transaction_id: str = Field(min_length=1, max_length=80)
    transaction_type: str = Field(default="SAVINGS", pattern="^SAVINGS$")
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class SyncRequest(BaseModel):
    transactions: list[SyncTransaction] = Field(min_length=1, max_length=50)


class SyncItemResponse(BaseModel):
    client_transaction_id: str
    status: str
    transaction_id: str | None = None
    message: str | None = None


class SyncResponse(BaseModel):
    items: list[SyncItemResponse]
