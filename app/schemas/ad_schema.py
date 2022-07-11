from typing import Union
from datetime import datetime
from pydantic import BaseModel


class AdBase(BaseModel):
    title: Union[str, None] = None
    body: str
    state: str

class AdCreate(AdBase):
    pass

class Ad(AdBase):
    id: int
    owner_id: int
    created_at = datetime
    updated_at = datetime

    class Config:
        orm_mode = True


