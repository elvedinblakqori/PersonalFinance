from dataclasses import dataclass
import os


@dataclass
class Settings:
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/expenses.db")


settings = Settings()
