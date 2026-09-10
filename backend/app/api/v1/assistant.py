import re

from fastapi import APIRouter, Depends

from app.db.dependencies import get_current_user
from app.models.user import User
from app.schemas.assistant import AssistantIntentRequest, AssistantIntentResponse

router = APIRouter(prefix="/assistant", tags=["Accessibility Assistant"])


def parse_amount(text: str) -> float | None:
    match = re.search(
        r"(?:₹|rs\.?|rs)\s*([0-9]+(?:\.[0-9]+)?)",
        text.lower(),
    )

    if not match:
        match = re.search(r"\b([0-9]+(?:\.[0-9]+)?)\b", text)

    return float(match.group(1)) if match else None


@router.post("/intent", response_model=AssistantIntentResponse)
def intent(
    payload: AssistantIntentRequest,
    current_user: User = Depends(get_current_user),
):
    text = payload.text.lower()
    amount = parse_amount(payload.text)

    if any(word in text for word in ["save", "savings", "சேமி", "சேமிப்பு"]):
        return AssistantIntentResponse(
            intent="SAVINGS",
            amount=amount,
            message="Savings request understood. Confirm the amount before submitting.",
        )

    if any(word in text for word in ["loan", "credit", "கடன்"]):
        return AssistantIntentResponse(
            intent="LOAN",
            amount=amount,
            message="Micro-credit request understood. Confirm the requested amount.",
        )

    return AssistantIntentResponse(
        intent="UNKNOWN",
        amount=amount,
        message="I could not safely identify the financial action.",
    )
