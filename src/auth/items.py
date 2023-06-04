# from typing import List
# from fastapi import Depends, HTTPException
#
# from fastapi import APIRouter
# from sqlalchemy.orm import Session
#
# import crud, role
# from auth.auth import auth_handler
# from database import get_db
# from auth import schemas
# from settings import settings
#
# router = APIRouter(tags=['items'])
#
# checking_for_moderator = role.RoleChecker(settings.moderator_list)
#
# active_user = auth_handler.auth_wrapper
#
#
# @router.post("/item/create/",
#              dependencies=[Depends(active_user)],
#              response_model=schemas.ItemCreate)
# def create_item(
#         item: schemas.ItemCreate,
#         db: Session = Depends(get_db),
#         user_id=Depends(active_user)):
#     return crud.create_item(db=db, item=item, user_id=user_id)
#
#
# @router.get("/items/{item_id}",
#             response_model=schemas.ItemAndUser)
# def read_item(
#         item_id: int,
#         db: Session = Depends(get_db)):
#     db_item = crud.get_item(db=db, item_id=item_id)
#     if db_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return db_item
#
#
# @router.get("/items/",
#             response_model=List[schemas.ItemAndUser],)
# def read_items(
#         skip: int = 0,
#         limit: int = 100,
#         db: Session = Depends(get_db)):
#     items = crud.get_items(db=db, skip=skip, limit=limit)
#     return items
#
#
# @router.delete("/items/delete/{item_id}",
#                dependencies=[Depends(checking_for_moderator)],)
# def delete_item(
#         item_id: int,
#         db: Session = Depends(get_db)):
#     return crud.delete_item(db=db, item_id=item_id)
#
#
# @router.put("/items/update/{item_id}",
#             dependencies=[Depends(active_user)])
# def update_item(
#         edit_item: schemas.ItemBase,
#         item_id: int,
#         db: Session = Depends(get_db),
#         user_id=Depends(active_user)):
#     item = crud.get_item(db=db, item_id=item_id)
#     user = crud.get_user(db=db, user_id=user_id)
#     if user_id == item.owner_id or user.role in settings.moderator_list:
#         return crud.update_item(db=db, item=item, edit_item=edit_item)
#     else:
#         raise HTTPException(status_code=401, detail='Not enough rights')
#
#
