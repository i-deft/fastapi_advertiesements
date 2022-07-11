from typing import Union
from datetime import datetime
from pydantic import BaseModel


class DraftBase(BaseModel):
    title: Union[str, None] = None
    body: str
    state: str


class DraftCreate(DraftBase):
    pass


class Draft(DraftBase):
    id: int
    owner_id: int
    created_at = datetime
    updated_at = datetime

    class Config:
        orm_mode = True


