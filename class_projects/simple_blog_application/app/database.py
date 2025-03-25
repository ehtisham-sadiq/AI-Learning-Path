from sqlalchemy import create_engine # establish connection with the database
from sqlalchemy.ext.declarative import declarative_base # declare the base for the models like ORM models
from sqlalchemy.orm import sessionmaker # create a session to the database
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/blog_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# engine is a connection object to the database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
