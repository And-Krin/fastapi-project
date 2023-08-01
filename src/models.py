from typing import Union
from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from fastapi_users.db import SQLAlchemyBaseUserTable

from settings import settings


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(length=32), unique=True, index=True)
    gender: Mapped[str] = mapped_column(String, default=settings.gender_default)
    role: Mapped[str] = mapped_column(String, default=settings.role_default)
    time_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[Union[datetime, None]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship(User, back_populates="items")



# class User(Base):
#     __tablename__ = "user"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(length=32), unique=True, index=True)
#     gender = Column(String, default=settings.gender_default)
#     is_active = Column(Boolean, default=True, nullable=False)
#     role = Column(String, default=settings.role_default)
#     time_created = Column(DateTime(timezone=True), server_default=func.now())
#     time_updated = Column(DateTime(timezone=True), onupdate=func.now())
#     email = Column(String(length=320), unique=True, index=True, nullable=False)
#     hashed_password = Column(String(length=1024), nullable=False)
#     is_superuser = Column(Boolean, default=False, nullable=False)
#     is_verified = Column(Boolean, default=False, nullable=False)
#
#     items = relationship("Item", back_populates="owner")





