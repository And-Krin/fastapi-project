from fastapi_users import schemas

from typing import Union, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr

from settings import settings

from users.schemas import UserRead


class ItemBase(BaseModel):
    title: Union[str, None] = None
    body: Union[str, None] = None

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):

    class Config:
        orm_mode = True


class ItemCreated(ItemCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ItemRead(ItemBase):
    id: int
    owner_id: int
    time_created: datetime
    time_updated: Union[datetime, None] = None

    class Config:
        orm_mode = True


class ItemAndUser(ItemRead):
    owner: UserRead

    class Config:
        orm_mode = True
