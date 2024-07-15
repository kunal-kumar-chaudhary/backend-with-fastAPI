from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# creating engine for connecting to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# creating base class for our models
Base = declarative_base()

# we will use this for creating local session when we need to interact with the database
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# creating a function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
