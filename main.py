from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas import user_schema, advertisement_schema
from app.functions import user_functions, advertisement_functions, dependencies
from app.db import models
from app.db.database import engine
from app import role_permissions as rp


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", response_model=list[advertisement_schema.AdvertisementToFeed])
def read_feed(skip: int = 0,
              limit: int = 100,
              db: Session = Depends(dependencies.get_db)):
    users = advertisement_functions.all_advertisements(db,
                                                       skip=skip,
                                                       limit=limit)
    return users


@app.post("/users/", response_model=user_schema.User, dependencies=[Depends(rp.allow_create_users)])
def create_user(user: user_schema.UserCreate,
                db: Session = Depends(dependencies.get_db),
                current_user: models.User = Depends(
                    dependencies.get_current_user),
                ):
    db_user = user_functions.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=200, detail="Email already registered")
    return user_functions.create_user(db=db, user=user)


@app.put("/users/{user_id}", response_model=user_schema.User, dependencies=[Depends(rp.allow_update_users)])
def update_user(user_id: int,
                user_in: user_schema.UserUpdate,
                db: Session = Depends(dependencies.get_db),
                current_user: models.User = Depends(
                    dependencies.get_current_user)):
    db_user = user_functions.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=200, detail="Email already registered")
    return user_functions.update_user(db=db, user_id=user_id, user_in=user_in)


@app.delete("/users/{user_id}", response_model=user_schema.User, dependencies=[Depends(rp.allow_delete_users)])
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = user_functions.get_user(db, user_id=user_id)
    if not db_user or not db_user.is_active:
        raise HTTPException(status_code=404, detail="User not found")
    return user_functions.delete_user(db=db, user=db_user)


@app.get("/users/", response_model=list[user_schema.User], dependencies=[Depends(rp.allow_view_users_list)])
def read_users(skip: int = 0,
               limit: int = 100,
               db: Session = Depends(dependencies.get_db),
               current_user: models.User = Depends(
                   dependencies.get_current_user)):
    users = user_functions.get_users(db=db, skip=skip, limit=limit, current_user=current_user)
    return users


@app.get("/users/{user_id}", response_model=user_schema.User)
def read_user(user_id: int,
              db: Session = Depends(dependencies.get_db),
              current_user: models.User = Depends(
                  dependencies.get_current_user)):
    db_user = user_functions.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/advertisements/",
          response_model=advertisement_schema.Advertisement, dependencies=[Depends(rp.allow_create_advertisements)])
def create_user_advertisement(
        user_id: int,
        advertisement: advertisement_schema.AdvertisementCreate,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user)):
    return advertisement_functions.create_user_advertisement(
        db=db, advertisement=advertisement, user_id=user_id, current_user=current_user)


@app.get("/users/{user_id}/advertisements/",
         response_model=list[advertisement_schema.Advertisement])
def read_user_advertisements(user_id: int,
                             skip: int = 0,
                             limit: int = 100,
                             db: Session = Depends(dependencies.get_db),
                             current_user: models.User = Depends(
                                 dependencies.get_current_user)):
    ads = advertisement_functions.get_advertisements(db,
                                                     skip=skip,
                                                     limit=limit,
                                                     user_id=user_id)
    return ads


@app.get("/users/{user_id}/drafts/",
         response_model=list[advertisement_schema.Advertisement])
def read_user_drafts(user_id: int,
                     skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(dependencies.get_db),
                     current_user: models.User = Depends(
                         dependencies.get_current_user)):
    moderator_has_acces = user_functions.check_moderator_access(user_id=user_id, current_user=current_user)
    if not moderator_has_acces:
        raise HTTPException(status_code=404, detail="Drafts not found")
    drafts = advertisement_functions.get_drafts(db,
                                                skip=skip,
                                                limit=limit,
                                                user_id=user_id,
                                                current_user=current_user)
    return drafts


@app.post("/users/{user_id}/drafts/",
          response_model=advertisement_schema.Advertisement, dependencies=[Depends(rp.allow_create_drafts)])
def create_user_draft(user_id: int,
                      draft: advertisement_schema.AdvertisementCreate,
                      db: Session = Depends(dependencies.get_db),
                      current_user: models.User = Depends(
                          dependencies.get_current_user)):
    return advertisement_functions.create_user_draft(db=db,
                                                     draft=draft,
                                                     user_id=user_id,
                                                     current_user=current_user
                                                     )


@app.get("/users/{user_id}/advertisements/{advertisement_id}",
         response_model=advertisement_schema.Advertisement)
def read_advertisement(advertisement_id: int,
                       user_id: int,
                       db: Session = Depends(dependencies.get_db),
                       current_user: models.User = Depends(
                           dependencies.get_current_user)):
    advertisement = advertisement_functions.get_advertisement(
        db, advertisement_id=advertisement_id, owner_id=user_id)
    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return advertisement


@app.get("/users/{user_id}/drafts/{draft_id}",
         response_model=advertisement_schema.Advertisement)
def read_draft(draft_id: int,
               user_id: int,
               db: Session = Depends(dependencies.get_db),
               current_user: models.User = Depends(
                   dependencies.get_current_user)):
    draft = advertisement_functions.get_draft(db,
                                              draft_id=draft_id,
                                              owner_id=user_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft


@app.put("/users/{user_id}/advertisements/{advertisement_id}",
         response_model=advertisement_schema.Advertisement, dependencies=[Depends(rp.allow_update_advertisements)])
def update_advertisement(
        advertisement_id: int,
        user_id: int,
        advertisement_in: advertisement_schema.AdvertisementUpdate,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user)):

    db_advertisement = advertisement_functions.get_advertisement(
        db, advertisement_id=advertisement_id, owner_id=user_id)
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return advertisement_functions.update_advertisement(
        db,
        db_advertisement=db_advertisement,
        owner_id=user_id,
        advertisement_in=advertisement_in)


@app.put("/users/{user_id}/drafts/{draft_id}",
         response_model=advertisement_schema.Advertisement, dependencies=[Depends(rp.allow_update_drafts)])
def update_draft(draft_id: int,
                 user_id: int,
                 draft_in: advertisement_schema.AdvertisementUpdate,
                 db: Session = Depends(dependencies.get_db),
                 current_user: models.User = Depends(
                     dependencies.get_current_user)):
    db_draft = advertisement_functions.get_draft(db,
                                                 draft_id=draft_id,
                                                 owner_id=user_id)
    if db_draft is None:
        raise HTTPException(status_code=404, detail="Draft not found")

    return advertisement_functions.update_draft(db,
                                                db_draft=db_draft,
                                                owner_id=user_id,
                                                draft_in=draft_in)


@app.post("/auth", response_model=user_schema.TokenBase)
def auth(form_data: OAuth2PasswordRequestForm = Depends(),
         db: Session = Depends(dependencies.get_db)):
    user = user_functions.get_user_by_email(db=db, email=form_data.username)

    if not user:
        raise HTTPException(status_code=400,
                            detail="Incorrect email or password")

    if not user_functions.verify_password(
            plain_password=form_data.password,
            hashed_password=user.hashed_password):
        raise HTTPException(status_code=400,
                            detail="Incorrect email or password")

    return user_functions.create_user_token(db=db, user_id=user.id)


@app.get("/user/me", response_model=user_schema.User)
def read_current_user(current_user: user_schema.User = Depends(
    dependencies.get_current_user)):
    return current_user
