from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from jose import jwt
from ..db import get_db
from .. import auth, schemas, models
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    '''creating access_token and refresh_token'''
    user = auth.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    access = auth.create_access_token(user.username)
    refresh = auth.create_refresh_token(user.username)
    user.refresh_token = refresh
    db.add(user)
    db.commit()
    return {"access_token": access, "refresh_token": refresh}


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(body: schemas.TokenRefreshRequest,
                  db: Session = Depends(get_db)):
    '''Refresh token'''
    try:
        payload = jwt.decode(body.refresh_token,
                             auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
    except Exception:
        raise HTTPException(401, "Invalid refresh token")
    user = db.exec(
        select(models.User).where(models.User.username == username)).first()
    if not user or user.refresh_token != body.refresh_token:
        raise HTTPException(401, "Refresh token invalid or revoked")
    new_access = auth.create_access_token(username)
    new_refresh = auth.create_refresh_token(username)
    user.refresh_token = new_refresh
    db.add(user)
    db.commit()
    return {"access_token": new_access, "refresh_token": new_refresh}


