from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from db.database import SessionLocal
from .user_functions import get_user_by_token
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth", auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_user_by_token(db=db, token=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user
