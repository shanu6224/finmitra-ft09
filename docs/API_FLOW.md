# FT-09 API flow

## Registration
POST /api/v1/auth/register

Creates:
User -> Account

## Login
POST /api/v1/auth/login

Returns JWT bearer token.

## Savings
POST /api/v1/savings

The backend:
1. authenticates user
2. finds account
3. validates amount
4. checks client_transaction_id
5. updates balance
6. records transaction
7. writes audit log

## Offline sync
POST /api/v1/sync/transactions

A mobile client sends queued transactions after connectivity returns.

Possible result:
- SYNCED
- ALREADY_PROCESSED
- FAILED_RETRY

The unique client_transaction_id prevents a retry from creating a second financial transaction.

## Accessibility assistant
POST /api/v1/assistant/intent

The assistant interprets text into an intent. It does NOT mutate the account.

The frontend must show a confirmation screen before calling a financial mutation endpoint.
