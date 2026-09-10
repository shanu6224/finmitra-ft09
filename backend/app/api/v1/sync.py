from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.dependencies import get_current_user
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.savings import SyncRequest, SyncResponse, SyncItemResponse
from app.services.savings_service import create_savings

router = APIRouter(prefix="/sync", tags=["Offline Sync"])


@router.post("/transactions", response_model=SyncResponse)
def sync_transactions(
    payload: SyncRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = db.scalar(select(Account).where(Account.user_id == current_user.id))
    results = []

    for item in payload.transactions:
        try:
            transaction, status = create_savings(
                db,
                account,
                item.amount,
                item.client_transaction_id,
            )
            results.append(
                SyncItemResponse(
                    client_transaction_id=item.client_transaction_id,
                    status=status,
                    transaction_id=transaction.id,
                    message="Server confirmed" if status == "SYNCED" else "Duplicate safely ignored",
                )
            )
        except Exception:
            db.rollback()
            results.append(
                SyncItemResponse(
                    client_transaction_id=item.client_transaction_id,
                    status="FAILED_RETRY",
                    message="Temporary server error; retry this item",
                )
            )

    account.last_synced_at = datetime.now(timezone.utc)
    db.commit()
    return SyncResponse(items=results)
