from typing import List, Union, Literal
from datetime import datetime

from pydantic import BaseModel


# class AuthDetails(BaseModel):
#     username: str
#     password: str


class ItemBase(BaseModel):
    title: Union[str, None] = None
    body: Union[str, None] = None


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


class UserCreate(UserBase):
    password: str


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
    items: List[Item] = []

    class Config:
        orm_mode = True


class NewItem(Item):
    owner: UserBase

    class Config:
        orm_mode = True

