from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from schemas import user_schema
from functions import user_functions
from db import models
from db.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_functions.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_functions.create_user(db=db, user=user)


@app.get("/users/", response_model=list[user_schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_functions.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_functions.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @app.post("/users/{user_id}/news/", response_model=user_schema.News)
# def create_item_for_user(
#     user_id: int, news: user_schema.NewsCreate, db: Session = Depends(get_db)
# ):
#     return user_functions.create_user_item(db=db, news=news, user_id=user_id)
#

# @app.get("/items/", response_model=list[user_schema.News])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     news = user_functions.get_news(db, skip=skip, limit=limit)
#     return news

@app.put("/users/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, user: user_schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_functions.get_user_by_email(db, email=user.email)
    return user_functions.update_user(db=db, user=user, user_id=user_id)
