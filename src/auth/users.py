import sys

from typing import List, Literal, Optional
from fastapi import Depends, HTTPException, Form

from fastapi import APIRouter
# from .. import schemas, crud
from sqlalchemy.orm import Session
# from ..main import get_db, auth_handler

# sys.path.append(r'/sql_app')
from auth import schemas
import crud, role
from database import get_db
from auth.auth import auth_handler

router = APIRouter(tags=['users'])

role_admin = role.RoleChecker(["admin"])
role_moderator = role.RoleChecker(["moderator", "admin"])

current_user = auth_handler.auth_wrapper

role_list = Literal["user", "moderator", "admin"]
gender_list = Literal["undefined", "man", "woman"]

# @router.get("/users_sys/")
# def get_path():
#     return sys.path


@router.post("/user/",
             response_model=schemas.User)
def create_user(
        gender: gender_list,
        user: schemas.UserCreate,
        role: role_list = "user",
        db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user, gender=gender, role_user=role)


@router.get("/users/",
            response_model=List[schemas.User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}",
            response_model=schemas.User)
def read_user(
        user_id: int,
        db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/update/{user_id}",
            dependencies=[Depends(current_user)])
def update_user(
        edit_user: schemas.UserCreate,
        gender: gender_list,
        is_active: bool,
        user_id: int,
        this_user_id: schemas.User = Depends(current_user),
        role: role_list = "user",
        db: Session = Depends(get_db),):
    user = crud.get_user(db=db, user_id=user_id)
    this_user = crud.get_user(db=db, user_id=this_user_id)
    if user_id != this_user.id:
        if this_user.role != "admin":
            raise HTTPException(status_code=401, detail='Not enough rights')
        raise HTTPException(status_code=401, detail='Not enough rights')
    db_user = crud.get_user_by_username(db=db, username=edit_user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    if role != user.role:
        if this_user.role == "admin":
            return crud.update_user(
                db=db, user_id=user_id, gender=gender, is_active=is_active, role_user=role, edit_user=edit_user)
        else:
            raise HTTPException(status_code=401, detail='Not enough rights')
    else:
        return crud.update_user(
            db=db, user_id=user_id, gender=gender, is_active=is_active, role_user=role, edit_user=edit_user)


# @router.put("/users/update/{user_id}",
#             dependencies=[Depends(role_admin)])
# def update_user(
#         edit_user: schemas.UserCreate,
#         gender: gender_list,
#         is_active: bool,
#         user_id: int,
#         role: role_list = "user",
#         db: Session = Depends(get_db),):
#     db_user = crud.get_user_by_username(db=db, username=edit_user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="username already registered")
#     return crud.update_user(
#             db=db, user_id=user_id, gender=gender, is_active=is_active, role_user=role, edit_user=edit_user)
