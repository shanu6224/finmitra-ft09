from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.transaction import Transaction
from app.services.audit_service import write_audit


def create_savings(
    db: Session,
    account: Account,
    amount: Decimal,
    client_transaction_id: str,
):
    existing = db.scalar(
        select(Transaction).where(
            Transaction.client_transaction_id == client_transaction_id
        )
    )
    if existing:
        return existing, "ALREADY_PROCESSED"

    transaction = Transaction(
        account_id=account.id,
        client_transaction_id=client_transaction_id,
        transaction_type="SAVINGS",
        amount=amount,
        status="CONFIRMED",
        synced_at=datetime.now(timezone.utc),
    )

    account.balance = account.balance + amount
    account.last_synced_at = datetime.now(timezone.utc)

    db.add(transaction)
    write_audit(
        db,
        user_id=account.user_id,
        action="SAVINGS_CREATED",
        entity_type="TRANSACTION",
        entity_id=transaction.id,
    )
    db.commit()
    db.refresh(transaction)

    return transaction, "SYNCED"
