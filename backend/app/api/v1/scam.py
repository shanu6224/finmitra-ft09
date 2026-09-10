from fastapi import APIRouter

from app.schemas.scam import ScamAnalysisRequest, ScamAnalysisResponse
from app.services.scam_service import analyze_scam

router = APIRouter(prefix="/scam", tags=["Scam Detection"])


@router.post("/analyze", response_model=ScamAnalysisResponse)
def scam_analysis(payload: ScamAnalysisRequest):
    return analyze_scam(payload.text)