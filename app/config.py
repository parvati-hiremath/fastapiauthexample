from dotenv import load_dotenv
import os


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "2730ba64c791156ebd7bc2c24e3b601ffe9891429bb64a5d3df4258f6f968249")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
ACCESS_EXPIRE_MIN = int(os.getenv("ACCESS_EXPIRE_MIN", 30))
REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_EXPIRE_DAYS", 7))
