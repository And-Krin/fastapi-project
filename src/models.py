from typing import Union, AsyncGenerator
from datetime import datetime

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from settings import settings

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

metadata = MetaData()


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


table_users = User.__table__

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


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship(User, back_populates="items")


table_items = Item.__table__
# async def create_db_and_tables():
#     print('CREATE DATABASE')
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
#
#
# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)
