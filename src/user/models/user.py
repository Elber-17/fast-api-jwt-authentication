from sqlalchemy import Column, Integer, String

from core.sql_db.db import Base


class User(Base):
    __tablename__ = "user"

    id_ = Column("id", Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
