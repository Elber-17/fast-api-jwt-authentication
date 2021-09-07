from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm.session import Session

from core.sql_db.db import get_db

from core.security.oauth2_jwt import OAuth2JWT
from core.security.oauth2_jwt.schemas import (
    OAuth2JWTLogin as OAuth2JWTSchema,
    CreatedToken,
)

user_router = APIRouter(tags=["User"])


@user_router.post("/admin/login", response_model=CreatedToken)
async def user_login(
    body: OAuth2JWTSchema, db: Session = Depends(get_db)
) -> CreatedToken:
    o_auth2_jwt = OAuth2JWT()
    access_token = o_auth2_jwt.autenticate_user(db, body.username, body.password)

    return CreatedToken(**{"type": "Bearer", "access_token": access_token})


@user_router.post("/admin/openapi-login", response_model=CreatedToken)
async def user_openapi_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> CreatedToken:
    o_auth2_jwt = OAuth2JWT()
    access_token = o_auth2_jwt.autenticate_user(
        db, form_data.username, form_data.password
    )

    return CreatedToken(**{"type": "Bearer", "access_token": access_token})
