from sqlalchemy.orm import Session, joinedload
import models, role
from auth import schemas
from auth.auth import AuthHandler

auth_handler = AuthHandler()

active_user = auth_handler.auth_wrapper


def get_items_join_users(db: Session, page: int = 0, limit: int = 100):
    return db.query(models.Item).options(joinedload(models.Item.owner)).offset(page * limit - limit).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate, gender: str, role_user: str):
    hashed_password = auth_handler.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        gender=gender,
        role=role_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def delete_item(db: Session, item_id: int):
    item = get_item(db=db, item_id=item_id)
    db.delete(item)
    db.commit()
    return {item_id: 'deleted'}


def switch_user(db: Session, user_id: int):
    user = get_user(db=db, user_id=user_id)
    user.is_active = not user.is_active
    if user.is_active:
        state = "restored"
    else:
        state = "deleted"
    db.commit()
    db.refresh(user)
    return f"User {user.username} is {state}"


def update_item(db: Session,
                item: dict,
                edit_item: schemas.ItemBase,):
    item.title = edit_item.title
    item.body = edit_item.body
    db.commit()
    db.refresh(item)
    return {'id': item.id, 'title': item.title, 'body': item.body}


def update_user(db: Session,
                user_id: int,
                gender: str,
                is_active: bool,
                role_user: str,
                edit_user: schemas.UserCreate):
    hashed_password = auth_handler.get_password_hash(edit_user.password)
    user = get_user(db=db, user_id=user_id)
    user.username = edit_user.username
    user.hashed_password = hashed_password
    user.gender = gender
    user.is_active = is_active
    user.role = role_user
    db.commit()
    db.refresh(user)
    return {
            'id': user.id,
            'username': user.username,
            'is_active': user.is_active,
            'role': user.role,
            'gender': user.gender,
            }
