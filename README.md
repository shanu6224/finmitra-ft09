# FinAccess — FT-09 Backend Prototype

Backend for the INFINIX'26 FT-09 Digital Financial Inclusion Platform.

## Current backend scope

- JWT authentication
- Password hashing
- User/account creation
- Savings + balance
- Transaction history
- Offline transaction sync endpoint
- Idempotency using `client_transaction_id`
- Duplicate-safe retry behavior
- Simulated micro-credit eligibility/application
- Insurance information API
- Voice/text assistant intent parsing
- Audit log model
- PostgreSQL
- FastAPI Swagger docs

## Architecture

React Native / Expo
        |
        v
    FastAPI
        |
        v
   PostgreSQL

Offline transactions are queued by the mobile app and submitted to:
POST /api/v1/sync/transactions

## Run on Windows

### 1. Start PostgreSQL

Recommended for the prototype:

    docker compose up -d postgres

### 2. Create backend environment

    cd backend
    python -m venv venv
    venv\Scripts\activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Create `.env`

Copy `.env.example` to `.env` and change `SECRET_KEY`.

### 5. Start API

    uvicorn app.main:app --reload

Open:

    http://127.0.0.1:8000/docs

Health check:

    http://127.0.0.1:8000/health

## Important prototype rule

Financial actions are never executed directly by the assistant. The assistant only returns an intent and parameters. The user must confirm, then the normal savings/loan API performs validation and persistence.

## Next build order

1. Add Alembic migrations
2. Add stronger validation and authorization
3. Add proper service-layer tests
4. Add frontend integration
5. Add SQLite local queue in the React Native app
6. Add scam analysis endpoint
7. Add production deployment
