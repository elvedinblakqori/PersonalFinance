from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.report import ChartOut, MonthlySummaryOut
from app.services.report_service import ExpenseAnalyzer

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly-summary", response_model=MonthlySummaryOut)
def get_monthly_summary(
    year: int = Query(default=datetime.now().year, ge=2000, le=2100),
    month: int = Query(default=datetime.now().month, ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analyzer = ExpenseAnalyzer(db, current_user.id)
    return analyzer.monthly_summary(year, month)


@router.get("/monthly-chart", response_model=ChartOut)
def get_monthly_chart(
    year: int = Query(default=datetime.now().year, ge=2000, le=2100),
    month: int = Query(default=datetime.now().month, ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analyzer = ExpenseAnalyzer(db, current_user.id)
    try:
        chart_path = analyzer.generate_monthly_pie_chart(year, month)
        return ChartOut(chart_path=chart_path)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
