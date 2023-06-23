from typing import List
from fastapi import Depends, HTTPException

from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import exc

from auth import schemas
import crud, role
from database import get_db
from auth.auth import auth_handler
from settings import settings

router = APIRouter(tags=['users'])

checking_for_admin = role.RoleChecker(settings.admin_list)

current_user = auth_handler.auth_wrapper
@router.get("/users/",
            response_model=List[schemas.UserAndItems])
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
        edit_user: schemas.UserUpdate,
        edit_user_id: int,
        new_password: str,
        request_user_id: schemas.User = Depends(current_user),
        db: Session = Depends(get_db),):
    try:
        user = crud.get_user(db=db, user_id=edit_user_id)
        request_user = crud.get_user(db=db, user_id=request_user_id)
        if request_user.role != settings.role_admin:
            if edit_user_id != request_user.id or edit_user.role != user.role:
                raise HTTPException(status_code=401, detail='Not enough rights')
        return crud.update_user(
            db=db, edit_user_id=edit_user_id, edit_user=edit_user, new_password=new_password)
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail="This username is already registered")

