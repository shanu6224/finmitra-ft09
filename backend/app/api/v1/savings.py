from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.dependencies import get_current_user
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.account import TransactionResponse
from app.schemas.savings import SavingsRequest
from app.services.savings_service import create_savings

router = APIRouter(prefix="/savings", tags=["Savings"])


@router.post("", response_model=TransactionResponse)
def save_money(
    payload: SavingsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = db.scalar(select(Account).where(Account.user_id == current_user.id))
    transaction, _ = create_savings(
        db, account, payload.amount, payload.client_transaction_id
    )
    return transaction


@router.get("/history", response_model=list[TransactionResponse])
def savings_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = db.scalar(select(Account).where(Account.user_id == current_user.id))
    return db.scalars(
        select(Transaction)
        .where(
            Transaction.account_id == account.id,
            Transaction.transaction_type == "SAVINGS",
        )
        .order_by(Transaction.created_at.desc())
    ).all()
