from fastapi import Depends,  HTTPException, status
from typing import List
from ..auth import get_current_active_user, get_current_user
from ..schemas import UserRole, UserOut
from .. import models
from fastapi import APIRouter
from sqlmodel import Session, select
from ..db import engine
from ..models import User


def require_role(*allowed_roles: UserRole):
    def wrapper(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
                )
        return current_user
    return wrapper


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[UserOut], dependencies=[Depends(require_role(UserRole.ADMIN, UserRole.EDITOR, UserRole.VIEWER))])
def list_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


@router.delete("/users/{user_id}", dependencies=[Depends(require_role(UserRole.ADMIN))])
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"message": "User deleted"}

'''def role_required(required_roles: List[UserRole]):
    def role_checker(current_user: models.User = Depends(
            get_current_active_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker


router = APIRouter(
    prefix="/role", tags=["role"]
)'''
'''

@router.post("/users/")
async def create_user(user: dict, current_user: models.User = Depends(role_required([UserRole.ADMIN, UserRole.EDITOR]))):
    return {"message": "user created", "user": user}'''

"""
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user: models.User = Depends(role_required([UserRole.ADMIN]))):
    return {"message": f"user{user_id} deleted"}"""

'''
@router.get("/users/")
async def read_users(current_user: models.User = Depends(role_required([UserRole.ADMIN, UserRole.EDITOR, UserRole.VIEWER]))):
    return {
        "user": {
         "id": current_user.id,
         "name": current_user.username,
         "role": current_user.role,
            }
    }'''
