from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=2, max_length=100)
    amount: float = Field(gt=0)
    expense_date: date
    notes: str = Field(default="", max_length=500)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, min_length=2, max_length=100)
    amount: float | None = Field(default=None, gt=0)
    expense_date: date | None = None
    notes: str | None = Field(default=None, max_length=500)


class ExpenseOut(ExpenseBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExpenseListOut(BaseModel):
    items: list[ExpenseOut]
    total: int
