from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.functions.user_functions import get_user_by_token
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth", auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)):
    user = get_user_by_token(db=db, token=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")
    return user


class RoleChecker:
    def __init__(self, allowed_roles: list, resource_owner: User = Depends(get_resource_owner)):
        self.allowed_roles = allowed_roles
        self.resource_owner = resource_owner

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")


