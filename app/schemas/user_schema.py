from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
from typing import Union


class UserBase(BaseModel):
    email: str
    role: Union[str, None] = 'client'


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    groups: list[Group] = []
    created_at: datetime
    updated_at: Union[datetime, None] = None

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    password: str
    is_active: Union[bool, None] = True


from .group_schema import Group
User.update_forward_refs()

