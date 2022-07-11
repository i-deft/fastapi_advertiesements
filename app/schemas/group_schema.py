from pydantic import BaseModel
from .user_schema import User


class GroupBase(BaseModel):
    region: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    owner_id: int
    users: list[User] = []

    class Config:
        orm_mode = True


