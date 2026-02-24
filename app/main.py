from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api import auth, expenses, external, reports
from app.db.database import Base, engine
from app.models import Expense, User
from app.web_page import get_homepage_html

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Finance Expense Tracker", version="1.0.0")

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(reports.router)
app.include_router(external.router)


@app.get("/")
def root():
    return HTMLResponse(content=get_homepage_html())
