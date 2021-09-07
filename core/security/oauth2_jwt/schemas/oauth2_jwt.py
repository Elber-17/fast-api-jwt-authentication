from pydantic import BaseModel, Field


class OAuth2JWTLogin(BaseModel):
    username: str
    password: str


class CreatedToken(BaseModel):
    type_: str = Field(..., alias="type")
    access_token: str

    class Config:
        allow_population_by_field_name = True
