from typing import Literal, List
from pydantic import BaseSettings


class Settings(BaseSettings):
    gender_list = Literal["Rather not say", "Male", "Female"]
    gender_default = "Rather not say"
    role_list = Literal["user", "moderator", "admin"]
    role_default = "user"
    role_admin = "admin"
    admin_list: List[str] = [role_admin]
    moderator_list: List[str] = admin_list + ["moderator"]


settings = Settings()
