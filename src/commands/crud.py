from sqlalchemy import insert
from sqlalchemy.orm import Session
from fastapi_users.password import PasswordHelper

from database import get_db
from models import User

password_helper = PasswordHelper()


def get_user_by_username(username: str):
    db: Session = next(get_db())
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(email: str):
    db: Session = next(get_db())
    return db.query(User).filter(User.email == email).first()


def create_user(username: str, email: str, role: str, password: str):
    db: Session = next(get_db())
    hashed_password = password_helper.hash(password=password)
    user = insert(User).values(
        username=username,
        email=email,
        is_active=True,
        is_superuser=False,
        is_verified=False,
        gender="Male",
        role=role,
        hashed_password=hashed_password,
    )
    db.execute(user)
    db.commit()
