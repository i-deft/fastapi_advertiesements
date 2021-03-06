from typing import Union
from datetime import datetime
from pydantic import BaseModel


class AdvertisementBase(BaseModel):
    title: Union[str, None] = None
    body: str


class AdvertisementCreate(AdvertisementBase):
    pass


class AdvertisementUpdate(AdvertisementBase):
    pass


class Advertisement(AdvertisementBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Union[datetime, None] = None
    state: str

    class Config:
        orm_mode = True


