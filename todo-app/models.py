from database import Base
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel, Field


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    desc = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    desc: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool
