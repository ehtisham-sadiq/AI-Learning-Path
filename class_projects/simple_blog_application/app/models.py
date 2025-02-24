from enum import unique
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, text, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

class EntityBase:
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=text('now()'))
    updated_at = Column(DateTime, nullable=False, default=text('now()'), onupdate=text('now()'))
    
class User(Base, EntityBase):
    __tablename__ = "users"
    
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)