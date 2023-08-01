from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_users import exceptions
from fastapi_users.router.common import ErrorCode, ErrorModel

import role
from database import get_async_session

from auth.manager import UserManager, get_user_manager
from settings import settings
from users import schemas
from models import User
from auth.base_config import current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

check_is_admin = role.RoleChecker(settings.admin_list)


async def get_user_or_404(
        id: str,
        user_manager: UserManager = Depends(get_user_manager),
) -> User:
    try:
        parsed_id = user_manager.parse_id(id)
        return await user_manager.get(parsed_id)
    except (exceptions.UserNotExists, exceptions.InvalidID) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e


@router.get("/",
            response_model=List[schemas.UserRead],
            name="users:all_users",
            )
async def read_users(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_async_session),
):
    query = select(User.__table__).offset(skip).limit(limit)
    result = await db.execute(query)
    result_all = result.all()
    return result_all


@router.get("/me",
            response_model=schemas.UserRead,
            name="users:current_user",
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Missing token or inactive user.",
                },
            },
            )
async def me(
        user: User = Depends(current_user),
):
    return schemas.UserRead.from_orm(user)


@router.put("/me",
            response_model=schemas.UserUpdate,
            dependencies=[Depends(current_user)],
            name="users:patch_current_user",
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Missing token or inactive user.",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "model": ErrorModel,
                    "content": {
                        "application/json": {
                            "examples": {
                                ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                                    "summary": "A user with this email already exists.",
                                    "value": {
                                        "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                                    },
                                },
                                ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                                    "summary": "Password validation failed.",
                                    "value": {
                                        "detail": {
                                            "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                            "reason": "Password should be"
                                            "at least 3 characters",
                                        }
                                    },
                                },
                            }
                        }
                    },
                },
            },
            )
async def update_me(
    request: Request,
    user_update: schemas.UserUpdate,  # type: ignore
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        user = await user_manager.update(
            user_update, user, safe=True, request=request
        )
        return schemas.UserUpdate.from_orm(user)
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        )


@router.get("/{user_id}",
            response_model=schemas.UserRead,
            )
async def read_user(
        user_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    query = select(User.__table__).where(User.id == user_id)
    result = await db.execute(query)
    db_user = result.first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{id}",
            response_model=schemas.UserRead,
            name="users:user",
            responses={
                    status.HTTP_401_UNAUTHORIZED: {
                        "description": "Missing token or inactive user.",
                    },
                    status.HTTP_403_FORBIDDEN: {
                        "description": "Not a superuser.",
                    },
                    status.HTTP_404_NOT_FOUND: {
                        "description": "The user does not exist.",
                    },
                },
            )
async def get_user(user=Depends(get_user_or_404)):
    return schemas.UserRead.from_orm(user)


@router.put("/{id}",
            response_model=schemas.UserUpdate,
            dependencies=[Depends(check_is_admin)],
            name="users:patch_user",
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Missing token or inactive user.",
                },
                status.HTTP_403_FORBIDDEN: {
                    "description": "Not a superuser.",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "The user does not exist.",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "model": ErrorModel,
                    "content": {
                        "application/json": {
                            "examples": {
                                ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                                    "summary": "A user with this email already exists.",
                                    "value": {
                                        "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                                    },
                                },
                                ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                                    "summary": "Password validation failed.",
                                    "value": {
                                        "detail": {
                                            "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                            "reason": "Password should be"
                                            "at least 3 characters",
                                        }
                                    },
                                },
                            }
                        }
                    },
                },
            },
            )
async def update_user(
    user_update: schemas.UserUpdate,  # type: ignore
    request: Request,
    user=Depends(get_user_or_404),
    user_manager: UserManager = Depends(get_user_manager),
    is_me: User = Depends(current_user)
):
    try:
        if is_me.is_superuser:
            safe = False
        else:
            safe = True
        user = await user_manager.update(
            user_update, user, safe=safe, request=request
        )
        return schemas.UserUpdate.from_orm(user)
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        )
