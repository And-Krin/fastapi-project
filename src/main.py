# print(sys.path)
# sys.path.remove('.')
# print(sys.path)

# from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers

import models
from FU_auth.schemas import UserRead, UserCreate
from FU_auth.manager import get_user_manager
from FU_auth.FU_auth import auth_backend
from settings import settings

fastapi_users = FastAPIUsers[models.User, int](
    get_user_manager,
    [auth_backend],
)
#
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
## app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])
# app.add_middleware(DBSessionMiddleware, db_url='postgresql://postgres:postgres@postgresql/test')
app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)

# app.include_router(users.router)
# app.include_router(items.router)
# app.include_router(auth.router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

from FU_auth.database import create_db_and_tables
create_db_and_tables()
