from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id_: int = Field(..., alias="id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserWithPassword(User):
    hashed_password: str

    class Config:
        orm_mode = True


class UserFindCondition(BaseModel):
    id_: int = Field(None, alias="id")
    username: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
