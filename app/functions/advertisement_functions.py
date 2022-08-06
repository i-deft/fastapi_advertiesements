from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import advertisement_schema
from app.db import models


def all_advertisements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Advertisement).order_by(
        models.Advertisement.created_at.desc()).offset(skip).limit(
            limit).all()


def get_drafts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Advertisement).filter_by(
        owner_id=user_id, state='draft').offset(skip).limit(limit).all()


def get_advertisement(db: Session, advertisement_id: int, owner_id: int):
    return db.query(models.Advertisement).filter_by(id=advertisement_id,
                                                    owner_id=owner_id).first()


def get_draft(db: Session, draft_id: int, owner_id: int):
    return db.query(models.Advertisement).filter_by(id=draft_id,
                                                    owner_id=owner_id).first()


def create_user_advertisement(
        db: Session, advertisement: advertisement_schema.AdvertisementCreate,
        user_id: int, current_user: models.User):
    if user_id != current_user.id and current_user.role == 'client':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    if user_id != current_user.id and current_user.role in [
            'admin', 'moderator'
    ]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Operation not permitted")
    db_ad = models.Advertisement(**advertisement.dict(),
                                 owner_id=user_id,
                                 state='active')
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad


def create_user_draft(db: Session,
                      draft: advertisement_schema.AdvertisementCreate,
                      user_id: int, current_user: models.User):
    db_draft = models.Advertisement(**draft.dict(),
                                    owner_id=user_id,
                                    state='draft')
    if user_id != current_user.id and current_user.role == 'client':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    elif current_user.role in ['admin', 'moderator']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Operation not permitted")
    db.add(db_draft)
    db.commit()
    db.refresh(db_draft)
    return db_draft


def update_draft(db: Session,
                 draft_in: advertisement_schema.AdvertisementUpdate,
                 owner_id: int, db_draft: models.Advertisement):
    db_draft.title, db_draft.body, db_draft.owner_id = draft_in.title, draft_in.body, owner_id
    db_draft.state = 'draft'
    db.add(db_draft)
    db.commit()
    db.refresh(db_draft)
    return db_draft


def update_advertisement(
        db: Session,
        advertisement_in: advertisement_schema.AdvertisementUpdate,
        owner_id: int, db_advertisement: models.Advertisement):
    db_advertisement.title, db_advertisement.body, db_advertisement.owner_id = advertisement_in.title, advertisement_in.body, owner_id
    db_advertisement.state = 'active'
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement
