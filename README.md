# ntr-order-handler

## Setup
Environment variables include the following
- `DATABASE_USER` (default: `ntr`)
- `DATABASE_PASSWORD` (default: `hardpass`)
- `DATABASE_DB` (default: `ntr`)
- `DATABASE_PORT` (default: `5432`)

## Linting
Before pushing, make sure to run
```
black .
```
in root of project. Follow up by
```
flake8 .
```
to ensure correct linting.