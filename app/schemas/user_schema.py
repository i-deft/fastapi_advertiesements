from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, validator, UUID4, EmailStr, Field, root_validator
from typing import Union, Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    groups: list[int] = []
    role: Union[str, None] = 'client'

    @root_validator
    def check_client_group(cls, values):
        role = values.get('role')
        groups = values.get('groups')
        if role == 'client' and not groups:
            raise ValueError('Client user requires binded groups')
        return values


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Union[datetime, None] = None
    role: str
    groups: list[Group] = []

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    password: str
    is_active: Union[bool, None] = True
    role: str
    groups: list[int] = []

    @root_validator
    def check_client_group(cls, values):
        role = values.get('role')
        groups = values.get('group')
        if role == 'client' and not groups:
            raise ValueError('Client user requires binded groups')
        return values


class UserToFeed(UserBase):
    id: int
    created_at: datetime
    updated_at: Union[datetime, None] = None

    class Config:
        orm_mode = True


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
