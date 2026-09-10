from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.dependencies import get_current_user
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.loan import LoanApplication
from app.schemas.financial_summary import FinancialSummaryResponse
from app.models.user import User
from app.schemas.account import AccountResponse, TransactionResponse

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("", response_model=AccountResponse)
def get_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.scalar(select(Account).where(Account.user_id == current_user.id))


@router.get("/balance")
def get_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = db.scalar(select(Account).where(Account.user_id == current_user.id))
    return {
        "balance": account.balance,
        "currency": "INR",
        "last_synced_at": account.last_synced_at,
    }


@router.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = db.scalar(select(Account).where(Account.user_id == current_user.id))
    return db.scalars(
        select(Transaction)
        .where(Transaction.account_id == account.id)
        .order_by(Transaction.created_at.desc())
    ).all()
loan_applications = db.scalars(
        select(LoanApplication)
        .where(LoanApplication.user_id == current_user.id)
    ).all()

    total_savings = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == "SAVINGS"
    )

    pending_loans = sum(
        1
        for loan in loan_applications
        if loan.application_status in ["SUBMITTED", "REVIEW_REQUIRED"]
    )

    return FinancialSummaryResponse(
        balance=account.balance,
        currency="INR",
        total_savings=total_savings,
        total_transactions=len(transactions),
        loan_applications=len(loan_applications),
        pending_loans=pending_loans,
    )
