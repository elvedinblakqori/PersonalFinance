from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserRegister


class AuthService:
    @staticmethod
    def register_user(db: Session, payload: UserRegister) -> User:
        existing = db.query(User).filter(User.email == payload.email.lower()).first()
        if existing:
            raise ValueError("Email is already registered")

        user = User(
            email=payload.email.lower(),
            full_name=payload.full_name.strip(),
            hashed_password=hash_password(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User | None:
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
