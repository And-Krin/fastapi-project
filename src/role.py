from fastapi import Depends, HTTPException
from typing import List
import logging


from auth.base_config import current_user
from models import User


logger = logging.getLogger('logger')


class RoleChecker:
    def __init__(
            self,
            allowed_roles: List
    ):
        self.allowed_roles = allowed_roles

    def __call__(
            self,
            user: User = Depends(current_user),
    ):
        if user.role not in self.allowed_roles:
            logger.debug(f"User {user.username} with role {user.role} not in {self.allowed_roles}")
            print(logger)
            raise HTTPException(status_code=403, detail="Operation not permitted")

