from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .. import models, schemas, auth
from ..db import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/welcome")
def welcome():
    '''Returns welcome message'''
    return {"message": "welcome!  Try authentication flow"}


@router.post("/signup", response_model=schemas.UserOut)
def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    '''signup using username and password'''
    existing = db.exec(
        select(models.User).where(
            models.User.username == user_in.username,
            models.User.email == user_in.email,)).first()
    if existing:
        raise HTTPException(400, "Username already exists")
    user = models.User(
        username=user_in.username,
        email=user_in.email,  # new added
        role=user_in.role,  # new add
        hashed_password=auth.hash_password(user_in.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# new added
@router.get("/verify-token")
def verify_token_endpoint(current_user: models.User = Depends(auth.get_current_active_user)):
    """Verify the validity of the token and return user info"""
    return {
        "valid": True,
        "user": {
         "id": current_user.id,
         "name": current_user.username,
            }
    }


@router.get("/allusers", response_model=list[schemas.UserOut])
def get_users(current_user: models.User = Depends(
    auth.get_current_active_user),
              db: Session = Depends(get_db)):
    """Get all users"""
    return db.exec(select(models.User)).all()


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, current_user: models.User = Depends(
    auth.get_current_active_user),
             db: Session = Depends(get_db)):
    """Get one user by ID"""
    user = db.exec(
        select(models.User).filter(models.User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, update_user: schemas.UserCreate,
                current_user: models.User =
                Depends(auth.get_current_active_user),
                db: Session = Depends(get_db)):
    """Update a user"""
    db_user = db.exec(
        select(models.User).filter(models.User.id == user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = update_user.username
    db_user.email = update_user.email

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: models.User = Depends(
        auth.get_current_active_user), db: Session = Depends(get_db)):
    """Delete a user"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # if user.id == current_user.id:
    # raise HTTPException(status_code=400, detail="Cannot delete yourself")
    if user.id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="cannot delete other users")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
