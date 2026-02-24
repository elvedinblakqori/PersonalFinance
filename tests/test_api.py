from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app


def create_test_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_auth_and_expense_crud_flow():
    client = create_test_client()

    register_payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpass123",
    }
    register_response = client.post("/auth/register", json=register_payload)
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    expense_payload = {
        "title": "Groceries",
        "category": "Food",
        "amount": 54.5,
        "expense_date": str(date(2026, 2, 1)),
        "notes": "Weekly shopping",
    }
    create_response = client.post("/expenses/", json=expense_payload, headers=headers)
    assert create_response.status_code == 201
    expense_id = create_response.json()["id"]

    list_response = client.get("/expenses/", headers=headers)
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    update_response = client.patch(
        f"/expenses/{expense_id}",
        json={"amount": 60.0, "notes": "Updated"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["amount"] == 60.0

    delete_response = client.delete(f"/expenses/{expense_id}", headers=headers)
    assert delete_response.status_code == 200

    list_after_delete = client.get("/expenses/", headers=headers)
    assert list_after_delete.status_code == 200
    assert list_after_delete.json()["total"] == 0


def test_reports_monthly_summary_endpoint():
    client = create_test_client()

    client.post(
        "/auth/register",
        json={
            "email": "report@example.com",
            "full_name": "Report User",
            "password": "reportpass123",
        },
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "report@example.com", "password": "reportpass123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/expenses/",
        json={
            "title": "Bus",
            "category": "Transport",
            "amount": 20.0,
            "expense_date": "2026-02-10",
            "notes": "",
        },
        headers=headers,
    )

    summary_response = client.get(
        "/reports/monthly-summary?year=2026&month=2",
        headers=headers,
    )
    assert summary_response.status_code == 200
    data = summary_response.json()
    assert data["transaction_count"] == 1
    assert data["total_expense"] == 20.0
