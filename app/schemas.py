from pydantic import BaseModel
from enum import Enum  # new add


class UserRole(str, Enum):  # new add
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class UserCreate(BaseModel):
    username: str
    email: str  # new add
    role: str  # new add
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str  # new add
    role: str  # new add
    is_active: bool


class Config:
    orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    refresh_token: str
