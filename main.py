from __future__ import annotations

from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi

from config import Settings

from core.redis.pool_connection import init_redis_pool
from core.redis.repository import RedisRepository

from core.security.oauth2_jwt.oauth2_jwt import OAuth2JWT

from error_handlers.schemas.unauthorized import UnauthorizedError
from error_handlers import validation_error, bad_gateway, bad_request, unauthorized

from utils.remove_422 import remove_422s

from src.user.controller import user_router
from src.user.schemas import UserWithPassword as UserSchema

global_settings = Settings()

app = FastAPI()

app.include_router(user_router)

app.add_exception_handler(RequestValidationError, validation_error.handler)
app.add_exception_handler(bad_gateway.BadGatewayException, bad_gateway.handler)
app.add_exception_handler(bad_request.BadRequestException, bad_request.handler)
app.add_exception_handler(unauthorized.UnauthorizedException, unauthorized.handler)


@app.on_event("startup")
async def startup_event() -> None:
    app.state.redis = await init_redis_pool()
    app.state.redis_repo = RedisRepository(app.state.redis)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    app.state.redis.close()
    await app.state.redis.wait_closed()


@app.get("/protected")
async def protected_route(
    user: UserSchema = Depends(OAuth2JWT.get_autenticated_user),
) -> dict[str, str]:
    return {"Hello": "This route is protected by jwt"}


remove_422s(app)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}


def custom_openapi():
    try:

        del app.openapi_schema["components"]["schemas"][
            "Body_user_openapi_login_admin_openapi_login_post"
        ]  # delete the schema generate for openapi login form, unknow issue
    except:
        pass
    return app.openapi_schema


app.openapi = custom_openapi
