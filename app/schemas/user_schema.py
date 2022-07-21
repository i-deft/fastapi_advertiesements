from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, validator, UUID4, EmailStr, Field
from typing import Union, Optional


class UserBase(BaseModel):
    email: EmailStr
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


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        return value.hex


from .group_schema import Group
User.update_forward_refs()

