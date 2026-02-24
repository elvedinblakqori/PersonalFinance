from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


class ExpenseService:
    @staticmethod
    def create_expense(db: Session, owner_id: int, payload: ExpenseCreate) -> Expense:
        expense = Expense(owner_id=owner_id, **payload.model_dump())
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def list_expenses(
        db: Session,
        owner_id: int,
        category: str | None = None,
        min_amount: float | None = None,
        max_amount: float | None = None,
    ) -> list[Expense]:
        query = db.query(Expense).filter(Expense.owner_id == owner_id)

        if category:
            query = query.filter(Expense.category.ilike(category.strip()))
        if min_amount is not None:
            query = query.filter(Expense.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Expense.amount <= max_amount)

        return query.order_by(Expense.expense_date.desc(), Expense.id.desc()).all()

    @staticmethod
    def get_expense_or_none(db: Session, owner_id: int, expense_id: int) -> Expense | None:
        return (
            db.query(Expense)
            .filter(Expense.id == expense_id, Expense.owner_id == owner_id)
            .first()
        )

    @staticmethod
    def update_expense(db: Session, expense: Expense, payload: ExpenseUpdate) -> Expense:
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(expense, key, value)

        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def delete_expense(db: Session, expense: Expense) -> None:
        db.delete(expense)
        db.commit()
