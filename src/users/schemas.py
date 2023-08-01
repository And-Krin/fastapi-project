from fastapi_users import schemas

from typing import Union, Optional, List
from datetime import datetime

from pydantic import BaseModel, EmailStr

from settings import settings


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
                "is_superuser",
                "is_active",
                "is_verified",
                "oauth_accounts",
                "role"
            },
        )

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={
            "id"
        },
                         )


class ItemBase(BaseModel):
    title: Union[str, None] = None
    body: Union[str, None] = None

    class Config:
        orm_mode = True


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


class UserAndItems(UserRead):
    items: List[ItemBase] = []


class UserCreate(CreateUpdateDictModel):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    gender: settings.gender_list

    class Config:
        orm_mode = True


class UserUpdate(CreateUpdateDictModel):
    username: str
    password: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
    gender: settings.gender_list
    role: settings.role_list

    class Config:
        orm_mode = True

