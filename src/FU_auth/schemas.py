from fastapi_users import schemas

from typing import Union, Generic, List, Optional, TypeVar
from datetime import datetime

from pydantic import BaseModel, EmailStr

from settings import settings


class UserRead(schemas.BaseUser[int]):
    username: str
    id: int
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    gender: str
    role: str
    time_created: datetime
    time_updated: Union[datetime, None] = None

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    gender: settings.gender_list


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    password: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
    gender: settings.gender_list
    role: settings.role_list


class ItemBase(BaseModel):
    title: Union[str, None] = None
    body: Union[str, None] = None

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int
    time_created: datetime
    time_updated: Union[datetime, None] = None

    class Config:
        orm_mode = True


class ItemAndUser(Item):
    owner: UserRead


