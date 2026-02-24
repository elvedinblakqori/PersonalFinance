import argparse
from datetime import date
import json

import requests


API_URL = "http://127.0.0.1:8000"


def register(email: str, full_name: str, password: str):
    payload = {"email": email, "full_name": full_name, "password": password}
    response = requests.post(f"{API_URL}/auth/register", json=payload, timeout=10)
    print(response.status_code)
    print(json.dumps(response.json(), indent=2))


def login(email: str, password: str) -> str:
    payload = {"email": email, "password": password}
    response = requests.post(f"{API_URL}/auth/login", json=payload, timeout=10)
    response.raise_for_status()
    token = response.json()["access_token"]
    print("Login successful")
    return token


def add_expense(token: str, title: str, category: str, amount: float, expense_date: str, notes: str):
    payload = {
        "title": title,
        "category": category,
        "amount": amount,
        "expense_date": expense_date,
        "notes": notes,
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/expenses/", json=payload, headers=headers, timeout=10)
    print(response.status_code)
    print(json.dumps(response.json(), indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI helper for Expense Tracker API")
    sub = parser.add_subparsers(dest="command", required=True)

    register_parser = sub.add_parser("register")
    register_parser.add_argument("--email", required=True)
    register_parser.add_argument("--full-name", required=True)
    register_parser.add_argument("--password", required=True)

    login_parser = sub.add_parser("login")
    login_parser.add_argument("--email", required=True)
    login_parser.add_argument("--password", required=True)

    add_parser = sub.add_parser("add-expense")
    add_parser.add_argument("--token", required=True)
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--amount", required=True, type=float)
    add_parser.add_argument("--expense-date", default=str(date.today()))
    add_parser.add_argument("--notes", default="")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "register":
        register(args.email, args.full_name, args.password)
    elif args.command == "login":
        token = login(args.email, args.password)
        print(token)
    elif args.command == "add-expense":
        add_expense(args.token, args.title, args.category, args.amount, args.expense_date, args.notes)


if __name__ == "__main__":
    main()
