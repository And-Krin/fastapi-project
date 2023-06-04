from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend


cookie_transport = CookieTransport(cookie_name="FU_cookie", cookie_max_age=86400)


SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)