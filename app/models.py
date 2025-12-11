from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str  # new add
    role: str  # new add
    hashed_password: str
    refresh_token: Optional[str] = None
    is_active: bool = True
