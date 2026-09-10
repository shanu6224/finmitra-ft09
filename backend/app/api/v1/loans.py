from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.dependencies import get_current_user
from app.models.loan import LoanApplication
from app.models.user import User
from app.schemas.loan import (
    LoanApplicationRequest,
    LoanApplicationResponse,
    LoanEligibilityRequest,
    LoanEligibilityResponse,
)

router = APIRouter(prefix="/loans", tags=["Micro-Credit"])


MAX_SIMULATED_AMOUNT = 50000


@router.post("/check-eligibility", response_model=LoanEligibilityResponse)
def check_eligibility(payload: LoanEligibilityRequest):
    eligible = payload.requested_amount <= MAX_SIMULATED_AMOUNT

    return LoanEligibilityResponse(
        eligible=eligible,
        max_simulated_amount=MAX_SIMULATED_AMOUNT,
        reason=(
            "Within simulated prototype limit."
            if eligible
            else "Requested amount exceeds the prototype limit."
        ),
    )


@router.post("/apply", response_model=LoanApplicationResponse, status_code=201)
def apply_loan(
    payload: LoanApplicationRequest,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_application = db.scalar(
        select(LoanApplication).where(
            LoanApplication.user_id == current_user.id,
            LoanApplication.client_application_id == payload.client_application_id,
        )
    )

    if existing_application:
        response.status_code = 200
        return existing_application

    eligible = payload.requested_amount <= MAX_SIMULATED_AMOUNT

    application = LoanApplication(
        user_id=current_user.id,
        client_application_id=payload.client_application_id,
        purpose=payload.purpose,
        requested_amount=payload.requested_amount,
        eligibility_status="ELIGIBLE" if eligible else "NOT_ELIGIBLE",
        application_status="SUBMITTED" if eligible else "REVIEW_REQUIRED",
    )
    db.add(application)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(application)
    return application

@router.get("/history", response_model=list[LoanApplicationResponse])
def loan_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.scalars(
        select(LoanApplication)
        .where(LoanApplication.user_id == current_user.id)
        .order_by(LoanApplication.created_at.desc())
    ).all()
