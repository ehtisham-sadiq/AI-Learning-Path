from enum import unique
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, text, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

# 1. users
# 2. posts
# 3. votes

class EntityBase:
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=text('now()'))
    updated_at = Column(DateTime, nullable=False, default=text('now()'), onupdate=text('now()'))
    
class User(Base, EntityBase):
    __tablename__ = "users"
    
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    posts = relationship("Post", back_populates="owner")
    
class Post(Base, EntityBase):
    __tablename__ = "posts"
    
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, default=True)
    
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="posts")
    
    
class Vote(Base, EntityBase):
    __tablename__ = "votes"
    
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    