# from sqlalchemy.orm import Session
# import models
# from auth import schemas
# from auth.auth import AuthHandler
#
# auth_handler = AuthHandler()
#
# active_user = auth_handler.auth_wrapper
#
#
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
#
# def get_user_by_username(db: Session, username: str):
#     return db.query(models.User).filter(models.User.username == username).first()
#
#
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
#
#
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user(db: Session,
#                 user: schemas.UserCreate,
#                 role_user: str = "user"):
#     hashed_password = auth_handler.get_password_hash(user.password)
#     new_user = models.User(
#         username=user.username,
#         hashed_password=hashed_password,
#         gender=user.gender,
#         role=role_user)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
#
#
# def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
#
#
# def get_item(db: Session, item_id: int):
#     return db.query(models.Item).filter(models.Item.id == item_id).first()
#
#
# def delete_item(db: Session, item_id: int):
#     item = get_item(db=db, item_id=item_id)
#     db.delete(item)
#     db.commit()
#     return {item_id: 'deleted'}
#
#
# def update_item(db: Session,
#                 item: schemas.Item,
#                 edit_item: schemas.ItemBase,):
#     item.title = edit_item.title
#     item.body = edit_item.body
#     db.commit()
#     db.refresh(item)
#     return item
#
#
# def update_user(db: Session,
#                 edit_user_id: int,
#                 new_password: str,
#                 edit_user: schemas.UserUpdate):
#     hashed_password = auth_handler.get_password_hash(new_password)
#     user = get_user(db=db, user_id=edit_user_id)
#     user.hashed_password = hashed_password
#     for key, value in edit_user:
#         setattr(user, key, value)
#     db.commit()
#     db.refresh(user)
#     return user
