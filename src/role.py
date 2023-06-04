# from fastapi import Depends, HTTPException
# from typing import List
# import logging
#
#
# from auth import auth
# import crud
# from database import get_db
#
#
# auth_handler = auth.AuthHandler()
# logger = logging.getLogger('logger')
#
#
# class RoleChecker:
#     def __init__(self, allowed_roles: List):
#         self.allowed_roles = allowed_roles
#
#     def __call__(self, user_id=Depends(auth_handler.auth_wrapper), db=Depends(get_db)):
#         user = crud.get_user(db, user_id)
#         if user.role not in self.allowed_roles:
#             logger.debug(f"User {user.username} with role {user.role} not in {self.allowed_roles}")
#             print(logger)
#             raise HTTPException(status_code=403, detail="Operation not permitted")

