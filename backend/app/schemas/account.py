from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: str
    account_number: str
    balance: Decimal
    last_synced_at: datetime | None

    model_config = {"from_attributes": True}


class TransactionResponse(BaseModel):
    id: str
    client_transaction_id: str
    transaction_type: str
    amount: Decimal
    status: str
    created_at: datetime
    synced_at: datetime | None

    model_config = {"from_attributes": True}
