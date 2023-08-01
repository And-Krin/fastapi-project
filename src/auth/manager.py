from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.models import UserProtocol

from database import get_user_db
from models import User
from settings import settings
from users.schemas import UserUpdate


SECRET = settings.SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def update(
        self,
        user_update: UserUpdate,
        user: UserProtocol,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> UserProtocol:
        """
        Update a user.

        Triggers the on_after_update handler on success

        :param user_update: The UserUpdate model containing
        the changes to apply to the user.
        :param user: The current user to update.
        :param safe: If True, sensitive values like is_superuser, is_verified or role
        will be ignored during the update, defaults to False
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :return: The updated user.
        """
        if safe:
            updated_user_data = user_update.create_update_dict()
        else:
            updated_user_data = user_update.create_update_dict_superuser()
        updated_user = await self._update(user, updated_user_data)
        await self.on_after_update(updated_user, updated_user_data, request)
        return updated_user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
