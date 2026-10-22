import os
from urllib.parse import quote
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./socialpilot.db"

# Render / Heroku postgres URL compatibility
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Safely encode passwords containing special characters (if not already percent-encoded)
if "://" in DATABASE_URL and "@" in DATABASE_URL:
    try:
        scheme, connection = DATABASE_URL.split("://", 1)
        if "@" in connection:
            credentials, host = connection.rsplit("@", 1)
            if ":" in credentials:
                username, password = credentials.split(":", 1)
                if "%" not in password:
                    DATABASE_URL = f"{scheme}://{username}:{quote(password, safe='')}@{host}"
    except Exception:
        pass

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()