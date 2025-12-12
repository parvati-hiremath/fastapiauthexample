#  FasrApi Authentication Example
This project demonstrates a simple authentication system built with **FastAPI**.  
It includes user registration, login, JWT-based authentication, and protected routes.

## Features
- User registration
- User login
- Password hashing
- JWT access tokens
- Protected API endpoints
- SQLModel / SQLAlchemy database support

##  Installation
###  Clone the repository
'''bash
git clone https://github.com/parvati-hiremath/fastapiauthexample.git
cd fastapiexample
#### create virtual-environment
'''bash
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
### Create Config.py
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
ACCESS_EXPIRE_MIN = int(os.getenv("ACCESS_EXPIRE_MIN", 30))
REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_EXPIRE_DAYS", 7)
### Install Dependencies(pyproject.toml)
pip install .
### Running fastapi
uvicorn app.main:app --reload
<img width="1920" height="998" alt="Screenshot from 2025-12-12 12-16-23" src="https://github.com/user-attachments/assets/28b15fab-7126-470a-a57e-d4a4a48ec670" />




