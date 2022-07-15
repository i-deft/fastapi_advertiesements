from sqlalchemy.orm import Session
from schemas import advertisement_schema
from db import models



def get_advertisements(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Ad).filter_by(owner_id=user_id, state='active').offset(skip).limit(limit).all()


def get_drafts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Ad).filter_by(owner_id=user_id, state='draft').offset(skip).limit(limit).all()

def create_user_advertisement(db: Session, advertisement: advertisement_schema.AdvertisementCreate, user_id: int):
    db_ad = models.Advertisement(**advertisement.dict(), owner_id=user_id)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad


