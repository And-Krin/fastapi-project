from typing import Literal, List
from pydantic import BaseSettings
import config as conf

URL = f"//{conf.DB_USER}:{conf.DB_PASS}@{conf.DB_HOST}:{conf.DB_PORT}/{conf.DB_NAME}"
URL_TEST = f"//{conf.DB_USER_TEST}:{conf.DB_PASS_TEST}@{conf.DB_HOST_TEST}:{conf.DB_PORT_TEST}/{conf.DB_NAME_TEST}"


class Settings(BaseSettings):
    DATABASE_URL = f"postgresql+asyncpg:{URL}"
    DATABASE_URL_TEST = f"postgresql+asyncpg:{URL_TEST}"
    SECRET = conf.SECRET
    gender_list = Literal["Rather not say", "Male", "Female"]
    gender_default = "Rather not say"
    role_list = Literal["user", "moderator", "admin"]
    role_default = "user"
    role_admin = "admin"
    admin_list: List[str] = [role_admin]
    moderator_list: List[str] = admin_list + ["moderator"]


settings = Settings()
