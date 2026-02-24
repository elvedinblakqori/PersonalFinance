from pydantic import BaseModel


class CategoryBreakdownItem(BaseModel):
    category: str
    total_amount: float


class MonthlySummaryOut(BaseModel):
    month: str
    total_expense: float
    transaction_count: int
    average_expense: float
    top_category: str | None
    category_breakdown: list[CategoryBreakdownItem]


class ChartOut(BaseModel):
    chart_path: str
