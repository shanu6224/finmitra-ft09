from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.dependencies import get_current_user
from app.models.insurance import InsuranceInformation
from app.models.user import User
from app.schemas.insurance import InsuranceResponse

router = APIRouter(prefix="/insurance", tags=["Insurance Information"])


@router.get("", response_model=list[InsuranceResponse])
def insurance_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.scalars(
        select(InsuranceInformation)
        .where(InsuranceInformation.is_active.is_(True))
        .order_by(InsuranceInformation.category)
    ).all()
