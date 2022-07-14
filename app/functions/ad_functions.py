from sqlalchemy.orm import Session
from schemas import ad_schema
from db import models



def get_ads(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Ad).filter_by(owner_id=user_id, state='active').offset(skip).limit(limit).all()


def get_drafts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Ad).filter_by(owner_id=user_id, state='draft').offset(skip).limit(limit).all()

def create_user_ad(db: Session, ad: ad_schema.AdCreate, user_id: int):
    db_ad = models.Ad(**ad.dict(), owner_id=user_id)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad


