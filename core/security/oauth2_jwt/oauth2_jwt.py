from datetime import datetime, timedelta
from typing import Optional

from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from jose import jwt, JWTError, ExpiredSignatureError

from config import Settings

from src.user.repository import UserRepository
from src.user.schemas import UserFindCondition, User as UserSchema

from core.security.bcrypt import verify_password

from error_handlers.bad_request import BadRequestException
from error_handlers.unauthorized import UnauthorizedException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/openapi-login")


class OAuth2JWT:
    settings = Settings()

    def autenticate_user(
        self, db: Session, email: str, password: str
    ) -> Optional[str]:
        findCondition: UserFindCondition = UserFindCondition(**{"email": email})
        user = UserRepository().findOne(db, findCondition)

        if not user or not verify_password(password, user.hashed_password):
            raise BadRequestException(message="Username or password is incorrect")

        return self.create_access_token(user_id=user.id_, username=user.username)

    def create_access_token(self, *, user_id: int, username: str) -> Optional[str]:
        return jwt.encode(
            {
                "id": user_id,
                "username": username,
                "exp": datetime.utcnow() + timedelta(minutes=15),
            },
            self.settings.jwt_secret,
            self.settings.jwt_algorithm,
        )

    @classmethod  # Definida como metodo de clase para ser usada como dependencia
    def get_autenticated_user(
        cls, token: str = Depends(oauth2_scheme)
    ) -> Optional[UserSchema]:
        try:
            payload = jwt.decode(
                token, cls.settings.jwt_secret, cls.settings.jwt_algorithm
            )
            username = payload.get("username")
            id_ = payload.get("id")

            if not username:
                raise UnauthorizedException

            return UserSchema(**{"id": id_, "username": username})

        except (JWTError, jwt.JWTClaimsError):
            UnauthorizedException(message="invalid Token")

        except ExpiredSignatureError:
            UnauthorizedException(message="the token has expired")
