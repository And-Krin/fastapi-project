from typing import List, Union
from datetime import datetime
from settings import settings

from pydantic import BaseModel


# class AuthDetails(BaseModel):
#     username: str
#     password: str


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


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    password: str


class UserCreate(UserLogin):
    gender: settings.gender_list


class UserUpdate(UserBase):
    gender: settings.gender_list
    is_active: bool
    role: settings.role_list


class UserGetPass(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    is_active: bool
    gender: str
    role: str
    time_created: datetime

    class Config:
        orm_mode = True


class UserAndItems(User):
    items: List[ItemBase] = []


class ItemAndUser(Item):
    owner: UserBase


class NewItem(Item):
    owner: UserBase

