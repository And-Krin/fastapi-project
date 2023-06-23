from fastapi import FastAPI, Depends

from auth.base_config import fastapi_users, auth_backend, current_user
from models import User
from users.schemas import UserRead, UserCreate

from users.router import router as users_router
from items.router import router as items_router

app = FastAPI()

app.include_router(users_router)
app.include_router(items_router)
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

# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )

# from auth.database import create_db_and_tables
# create_db_and_tables()
@app.get("/protected-route")
async def protected_route(user: User = Depends(current_user)):
    print(user.id)
    return f"Hello, {user.username}"


