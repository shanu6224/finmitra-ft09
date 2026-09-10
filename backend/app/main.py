from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import account, assistant, auth, insurance, loans, savings, scam, sync
from app.core.config import settings
from app.db.database import Base, engine

# Import models so SQLAlchemy knows all tables before create_all.
from app.models import account as _account_model
from app.models import audit_log as _audit_model
from app.models import insurance as _insurance_model
from app.models import loan as _loan_model
from app.models import transaction as _transaction_model
from app.models import user as _user_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FinAccess — lightweight financial inclusion prototype API.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(account.router, prefix="/api/v1")
app.include_router(savings.router, prefix="/api/v1")
app.include_router(sync.router, prefix="/api/v1")
app.include_router(loans.router, prefix="/api/v1")
app.include_router(insurance.router, prefix="/api/v1")
app.include_router(assistant.router, prefix="/api/v1")
app.include_router(scam.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "project": "FinAccess",
        "status": "running",
        "message": "Financial access for underserved users.",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
