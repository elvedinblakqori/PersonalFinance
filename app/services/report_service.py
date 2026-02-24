from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy.orm import Session

from app.models.expense import Expense


class ExpenseAnalyzer:
    """OOP service class for analytics and visualization."""

    def __init__(self, db: Session, owner_id: int):
        self.db = db
        self.owner_id = owner_id

    def _fetch_month_expenses(self, year: int, month: int) -> list[Expense]:
        start = date(year, month, 1)
        end = date(year + (month // 12), (month % 12) + 1, 1)
        return (
            self.db.query(Expense)
            .filter(
                Expense.owner_id == self.owner_id,
                Expense.expense_date >= start,
                Expense.expense_date < end,
            )
            .all()
        )

    def monthly_summary(self, year: int, month: int) -> dict:
        expenses = self._fetch_month_expenses(year, month)

        if not expenses:
            return {
                "month": f"{year}-{month:02d}",
                "total_expense": 0.0,
                "transaction_count": 0,
                "average_expense": 0.0,
                "top_category": None,
                "category_breakdown": [],
            }

        records = [{"amount": item.amount, "category": item.category} for item in expenses]
        df = pd.DataFrame(records)
        by_category = df.groupby("category", as_index=False)["amount"].sum()
        by_category = by_category.sort_values("amount", ascending=False)

        category_breakdown = []
        for _, row in by_category.iterrows():
            category_breakdown.append(
                {
                    "category": str(row["category"]),
                    "total_amount": round(float(row["amount"]), 2),
                }
            )

        total = float(df["amount"].sum())
        count = int(len(df))
        average = float(df["amount"].mean())
        top_category = str(by_category.iloc[0]["category"])

        return {
            "month": f"{year}-{month:02d}",
            "total_expense": round(total, 2),
            "transaction_count": count,
            "average_expense": round(average, 2),
            "top_category": top_category,
            "category_breakdown": category_breakdown,
        }

    def generate_monthly_pie_chart(self, year: int, month: int, output_dir: str = "data/charts") -> str:
        summary = self.monthly_summary(year, month)
        if not summary["category_breakdown"]:
            raise ValueError("No expense data found for the requested month")

        categories = [item["category"] for item in summary["category_breakdown"]]
        amounts = [item["total_amount"] for item in summary["category_breakdown"]]

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        filename = f"expense_pie_{self.owner_id}_{year}_{month:02d}.png"
        chart_file = output_path / filename

        plt.figure(figsize=(8, 8))
        plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
        plt.title(f"Expense Distribution {year}-{month:02d}")
        plt.tight_layout()
        plt.savefig(chart_file)
        plt.close()

        return str(chart_file)
