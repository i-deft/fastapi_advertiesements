from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.schemas import user_schema
from app.db import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter_by(id=user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session,
              current_user: models.User,
              skip: int = 0,
              limit: int = 100):
    if current_user.role == 'moderator':
        query = db.query(models.User).join(models.User, models.Group)
        return query.order_by(models.User.id).filter_by(
            is_active=True).offset(skip).limit(limit).all()
    elif current_user.role == 'admin':
        return db.query(models.User).order_by(models.User.id).filter_by(
        is_active=True).offset(skip).limit(limit).all()
    else:
        return [db.query(models.User).filter_by(id=current_user.id).first()]


def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if user.groups:
        for group_id in user.groups:
            db_group = db.query(models.Group).filter_by(id=group_id).first()
            db_user.groups.append(db_group)
    return db_user


def update_user(db: Session, user_id: int, user_in: user_schema.UserUpdate):
    user = get_user(db=db, user_id=user_id)
    hashed_password = get_password_hash(user_in.password)
    user.email = user_in.email
    user.hashed_password = hashed_password
    user.role = user_in.role
    user.is_active = user_in.is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: models.User):
    user.is_active = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_token(db: Session, token: str):
    query = db.query(models.User).join(models.Token).filter(
        models.Token.token == token,
        models.Token.expires > datetime.now()).first()
    return query


def create_user_token(db: Session, user_id: int):
    token = models.Token(expires=datetime.now() + timedelta(hours=1),
                         user_id=user_id)
    db.add(token)
    db.commit()
    db.refresh(token)
    token_dict = {"token": token.token, "expires": token.expires}
    return token_dict


def moderator_access(db: Session, current_user: models.User, user_id: int):
    if current_user.role != 'moderator':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                      detail="Operation not permitted")
    user = get_user(db=db, user_id=user_id)
    user_moderator = False
    for group in current_user.groups:
        if group in user.groups:
            user_moderator = True
    return user_moderator
