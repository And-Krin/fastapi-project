from typing import Literal, List
from pydantic import BaseSettings
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


class Settings(BaseSettings):
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    gender_list = Literal["Rather not say", "Male", "Female"]
    gender_default = "Rather not say"
    role_list = Literal["user", "moderator", "admin"]
    role_default = "user"
    role_admin = "admin"
    admin_list: List[str] = [role_admin]
    moderator_list: List[str] = admin_list + ["moderator"]


settings = Settings()
