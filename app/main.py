from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from schemas import user_schema, advertisement_schema
from functions import user_functions, advertisement_functions
from db import models
from db.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm

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
        raise HTTPException(status_code=200, detail="Email already registered")
    return user_functions.create_user(db=db, user=user)


@app.put("/users/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, user_in: user_schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_functions.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=200, detail="Email already registered")
    return user_functions.update_user(db=db, user_id=user_id, user_in=user_in)


@app.delete("/users/{user_id}", response_model=user_schema.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_functions.get_user(db, user_id=user_id)
    if not db_user or db_user.is_active == False:
        raise HTTPException(status_code=404, detail="User not found")
    return user_functions.delete_user(db=db, user=db_user)


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


@app.post("/users/{user_id}/advertisements/", response_model=advertisement_schema.Advertisement)
def create_user_advertisement(
        user_id: int, advertisement: advertisement_schema.AdvertisementCreate, db: Session = Depends(get_db)
):
    return advertisement_functions.create_user_advertisement(db=db, advertisement=advertisement, user_id=user_id)


@app.get("/users/{user_id}/advertisements/", response_model=list[advertisement_schema.Advertisement])
def read__user_advertisements(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ads = advertisement_functions.get_advertisements(db, skip=skip, limit=limit, user_id=user_id)
    return ads


@app.get("/users/{user_id}/drafts/", response_model=list[advertisement_schema.Advertisement])
def read__user_drafts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    drafts = advertisement_functions.get_drafts(db, skip=skip, limit=limit, user_id=user_id)
    return drafts


@app.post("/users/{user_id}/drafts/", response_model=advertisement_schema.Advertisement)
def create_user_draft(
        user_id: int, draft: advertisement_schema.AdvertisementCreate, db: Session = Depends(get_db)
):
    return advertisement_functions.create_user_draft(db=db, draft=draft, user_id=user_id)


@app.get("/users/{user_id}/advertisements/{advertisement_id}", response_model=advertisement_schema.Advertisement)
def read_advertisement(advertisement_id: int, user_id: int, db: Session = Depends(get_db)):
    advertisement = advertisement_functions.get_advertisement(db, advertisement_id=advertisement_id, owner_id=user_id)
    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return advertisement


@app.get("/users/{user_id}/drafts/{draft_id}", response_model=advertisement_schema.Advertisement)
def read_draft(draft_id: int, user_id: int, db: Session = Depends(get_db)):
    draft = advertisement_functions.get_draft(db, draft_id=draft_id, owner_id=user_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft


@app.put("/users/{user_id}/advertisements/{advertisement_id}", response_model=advertisement_schema.Advertisement)
def update_advertisement(advertisement_id: int, user_id: int,
                         advertisement_in: advertisement_schema.AdvertisementUpdate, db: Session = Depends(get_db)):
    db_advertisement = advertisement_functions.get_advertisement(db, advertisement_id=advertisement_id,
                                                                 owner_id=user_id)
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return advertisement_functions.update_advertisement(db, db_advertisement=db_advertisement, owner_id=user_id,
                                                        advertisement_in=advertisement_in)


@app.put("/users/{user_id}/drafts/{draft_id}", response_model=advertisement_schema.Advertisement)
def update_draft(draft_id: int, user_id: int, draft_in: advertisement_schema.AdvertisementUpdate,
                 db: Session = Depends(get_db)):
    db_draft = advertisement_functions.get_draft(db, draft_id=draft_id, owner_id=user_id)
    if db_draft is None:
        raise HTTPException(status_code=404, detail="Draft not found")

    return advertisement_functions.update_draft(db, db_draft=db_draft, owner_id=user_id, draft_in=draft_in)


@app.post("/auth", response_model=user_schema.TokenBase)
def auth(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_functions.get_user_by_email(db=db, email=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not user_functions.verify_password(
        plain_password=form_data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return user_functions.create_user_token(db=db, user_id=user.id)
