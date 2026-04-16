from dotenv import load_dotenv
load_dotenv()
# from user_app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
DATABASE_URL = os.getenv("DATABASE_URL")
print("DB URL:", DATABASE_URL)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # helps avoid stale connections
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()