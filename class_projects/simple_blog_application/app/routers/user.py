# 1. Get all the users
# 2. Get a single user by ID
# 3. Create a new user

from fastapi import APIRouter, Depends, status, HTTPException, Response, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models, utils, oauth2
from ..database import get_db
from ..models import User
from ..utils import hash_password

router = APIRouter(
    prefix="/v1/users",
    tags=["Users"]
)

@router.get("/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{user_id}", response_model=schemas.User)
def get_user(db: Session = Depends(get_db), user_id: int = Path(..., ge=1)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    check_if_exists(user, user_id)
    return user

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(db: Session = Depends(get_db), user: schemas.UserCreate = Depends(schemas.UserCreate)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def check_if_exists(user, user_id):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
