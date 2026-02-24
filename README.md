# Expense Tracker App (Python Advanced Project)

A full Personal Finance / Expense Tracker project that demonstrates:
- Variables, loops, conditional statements, functions, and data structures
- OOP with SQLAlchemy models and service classes
- Error handling and validation
- API development with FastAPI
- Web scraping for external exchange-rate data
- Database management with SQLite + SQLAlchemy
- Authentication and authorization with JWT
- Data manipulation and visualization using Pandas + Matplotlib
- Clear project structure, originality, and practical functionality

## Project Structure

```
app/
  api/            # API routers and dependencies
  core/           # config and security
  db/             # database setup
  models/         # SQLAlchemy ORM models
  schemas/        # Pydantic request/response schemas
  services/       # business logic
  utils/          # helper utilities
data/             # SQLite DB + generated charts
scripts/          # optional CLI client
tests/            # pytest tests
```

## Setup

```bash
py -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run API

```bash
uvicorn app.main:app --reload
```

Open docs at:
- http://127.0.0.1:8000/docs

## Main Flow

1. Register a user at `POST /auth/register`
2. Login at `POST /auth/login` to get a JWT token
3. Use token in `Authorize` button in Swagger docs
4. Create/read/update/delete expenses via `/expenses/*`
5. Get analytics and visualization via `/reports/*`
6. Fetch scraped exchange rate via `/external/exchange-rate`

## CLI (Optional)

```bash
python scripts/cli.py --help
```

## Run Tests

```bash
python -m pytest -q
```

## Useful Commands

Run API in background (PowerShell):

```powershell
Start-Process -FilePath ".\\.venv\\Scripts\\python.exe" -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000"
```

Stop API by PID:

```powershell
Stop-Process -Id <PID>
```
