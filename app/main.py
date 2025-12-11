from fastapi import FastAPI
from .db import engine
from .models import SQLModel
from .routers import users, auth_routes, protected, role

# title="SQLModel OAuth2 + Refresh Tokens Template"
app = FastAPI()


SQLModel.metadata.create_all(engine)


app.include_router(users.router)
app.include_router(auth_routes.router)
app.include_router(protected.router)
app.include_router(role.router)