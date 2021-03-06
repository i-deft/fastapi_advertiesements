from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from schemas import user_schema
from db import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter_by(id=user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).order_by(models.User.id).filter_by(is_active=True).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, role=user.role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_user_token(db=db, user_id=db_user.id)
    db.add(token)
    db.commit()
    db_user.token = token
    db.refresh(token)
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
    query = db.query(models.User, models.Token).filter(models.User.token == token, models.Token > datetime.now()).first()
    return query


def create_user_token(db: Session, user_id: int):
    token = models.Token(expires=datetime.now() + timedelta(hours=1), user_id=user_id)
    db.add(token)
    db.commit()
    db.refresh(token)
    token_dict = {"token": token.token, "expires": token.expires}
    return token_dict

