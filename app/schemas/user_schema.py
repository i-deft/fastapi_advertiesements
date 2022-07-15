from __future__ import annotations

from pydantic import BaseModel
from .advertisement_schema import Advertisement



class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    groups: list[Group] = []
    advertisements: list[Advertisement] = []

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    password: str
    is_active: bool
    email: str

from .group_schema import Group
User.update_forward_refs()

