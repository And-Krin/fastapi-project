from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

from database import get_user_db, get_async_session
from items import schemas
from models import Item, User
from auth.base_config import current_user

from settings import settings

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

# checking_for_moderator = role.RoleChecker(settings.moderator_list)
#
# active_user = auth_handler.auth_wrapper


@router.post("/create/",
             dependencies=[Depends(current_user)],
             response_model=schemas.ItemCreated,
             )
async def create_item(
        item: schemas.ItemCreate,
        user: User = Depends(current_user),
        db: AsyncSession = Depends(get_async_session)):
    print(user.id)
    stmt = Item.__table__.insert().values(**item.dict(), owner_id=user.id)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    result = await db.execute(stmt)
    await db.commit()
    return {**item.dict(), "id": int(result.inserted_primary_key.id), "owner_id": user.id}


@router.get("/",
            response_model=List[schemas.ItemRead],
            )
async def read_items(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_async_session)):
    query = select(Item.__table__).offset(skip).limit(limit)
    result = await db.execute(query)
    result_all = result.all()
    return result_all


@router.get("/{item_id}",
            response_model=schemas.ItemRead,
            )
async def read_item(
        item_id: int,
        db: AsyncSession = Depends(get_async_session)):
    query = select(Item.__table__).where(Item.id == item_id)
    result = await db.execute(query)
    db_item = result.first()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("=====>", db_item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete("/delete/{item_id}",
               dependencies=[Depends(current_user)],
               # dependencies=[Depends(checking_for_moderator)],
               )
async def delete_item(
        item_id: int,
        db: AsyncSession = Depends(get_async_session)):
    db_item = await read_item(item_id=item_id, db=db)
    stmt = Item.__table__.delete().where(Item.id == item_id)
    await db.execute(stmt)
    await db.commit()
    return {f"Item with id number:{db_item.id} removed"}


@router.put("/update/{item_id}",
            dependencies=[Depends(current_user)],
            response_model=schemas.ItemRead,
            )
async def update_item(
        edit_item: schemas.ItemBase,
        item_id: int,
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),):
    item = await read_item(item_id=item_id, db=db)
    if user.id == item.owner_id or user.role in settings.moderator_list:
        stmt = Item.__table__.update().values(**edit_item.dict()).where(Item.id == item_id)
        await db.execute(stmt)
        await db.commit()
        return await read_item(item_id=item_id, db=db)
    else:
        raise HTTPException(status_code=401, detail='Not enough rights')


