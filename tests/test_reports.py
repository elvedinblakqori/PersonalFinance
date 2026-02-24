class FakeExpense:
    def __init__(self, amount: float, category: str):
        self.amount = amount
        self.category = category


class FakeQuery:
    def __init__(self, items):
        self.items = items

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return self.items


class FakeDB:
    def __init__(self, items):
        self.items = items

    def query(self, _model):
        return FakeQuery(self.items)


from app.services.report_service import ExpenseAnalyzer


def test_monthly_summary_with_data():
    fake_db = FakeDB(
        [
            FakeExpense(10.0, "Food"),
            FakeExpense(20.0, "Transport"),
            FakeExpense(15.0, "Food"),
        ]
    )
    analyzer = ExpenseAnalyzer(fake_db, owner_id=1)
    summary = analyzer.monthly_summary(2026, 1)

    assert summary["transaction_count"] == 3
    assert summary["top_category"] == "Food"
    assert summary["total_expense"] == 45.0


def test_monthly_summary_without_data():
    fake_db = FakeDB([])
    analyzer = ExpenseAnalyzer(fake_db, owner_id=1)
    summary = analyzer.monthly_summary(2026, 1)

    assert summary["transaction_count"] == 0
    assert summary["total_expense"] == 0.0
    assert summary["category_breakdown"] == []
