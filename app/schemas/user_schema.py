from typing import Union
from pydantic import BaseModel
from .ad_schema import Ad
from .draft_schema import Draft
from .group_schema import Group


class UserBase(BaseModel):
    email: str
    users: list


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    news: list[Draft] = []
    notes: list[Ad] = []
    groups: list[Group] = []

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    password: str
    is_active: bool
    email: str
