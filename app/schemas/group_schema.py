from __future__ import annotations
from pydantic import BaseModel


class GroupBase(BaseModel):
    region: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    users: list[User] = []

    class Config:
        orm_mode = True


from .user_schema import User

Group.update_forward_refs()
