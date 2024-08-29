from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), nullable=False, unique=True)
    password = Column(String(1000), nullable=False)


class RequestUser(BaseModel):
    id: int = None
    user_name: str
    password: str


class ResponseUser(BaseModel):
    id: int
    user_name: str


class RequetTokenUser(BaseModel):
    token: str
