from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseListOut, ExpenseOut, ExpenseUpdate
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ExpenseService.create_expense(db, current_user.id, payload)


@router.get("/", response_model=ExpenseListOut)
def list_expenses(
    category: str | None = Query(default=None),
    min_amount: float | None = Query(default=None, ge=0),
    max_amount: float | None = Query(default=None, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(status_code=400, detail="min_amount cannot be greater than max_amount")

    items = ExpenseService.list_expenses(
        db=db,
        owner_id=current_user.id,
        category=category,
        min_amount=min_amount,
        max_amount=max_amount,
    )
    return ExpenseListOut(items=items, total=len(items))


@router.patch("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expense = ExpenseService.get_expense_or_none(db, current_user.id, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return ExpenseService.update_expense(db, expense, payload)


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expense = ExpenseService.get_expense_or_none(db, current_user.id, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    ExpenseService.delete_expense(db, expense)
    return {"message": "Expense deleted"}
