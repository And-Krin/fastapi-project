from fastapi_users import FastAPIUsers

from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
import models
from auth.manager import get_user_manager

cookie_transport = CookieTransport(cookie_name="FU_cookie", cookie_max_age=86400)


SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=86400)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[models.User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
