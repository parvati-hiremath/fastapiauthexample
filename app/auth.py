from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlmodel import select
from . import models
from .db import get_db
from .config import SECRET_KEY, ACCESS_EXPIRE_MIN, REFRESH_EXPIRE_DAYS

ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_token(data: dict, expires: timedelta):
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(username):
    return create_token({"sub": username}, timedelta(
       minutes=ACCESS_EXPIRE_MIN))


def create_refresh_token(username):
    return create_token({"sub": username}, timedelta(days=REFRESH_EXPIRE_DAYS))


def authenticate_user(db: Session, username: str, password: str):
    statement = select(models.User).where(models.User.username == username)
    user = db.exec(statement).first()
    if not user or not verify_password(password, user.hashed_password):
        return None

    return user


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    creds = HTTPException(
     status_code=status.HTTP_401_UNAUTHORIZED,
     detail="Could not validate credentials",
     headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise creds
    except JWTError:
        raise creds
    statement = select(models.User).where(models.User.username == username)
    user = db.exec(statement).first()
    if not user:
        raise creds
    return user


# new added
def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")

    return current_user

