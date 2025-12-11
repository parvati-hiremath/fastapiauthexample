from fastapi import APIRouter, Depends
from ..auth import get_current_user
from .. import models


router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/me")
def me(user: models.User = Depends(get_current_user)):
    '''protected end points that returns authenticated user details'''
    return {"id": user.id, "username": user.username}
