from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth.base_config import fastapi_users, auth_backend, current_user
from models import User
from users.schemas import UserRead, UserCreate

from users.router import router as users_router
from items.router import router as items_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(items_router)

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


@app.get("/protected-route")
async def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


