from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from ..database import get_db
from typing import Dict
from datetime import datetime

router = APIRouter(
    prefix="/v1/db",
    tags=['Database']
)

@router.get("/", response_model=Dict[str, str])
def get_db_status(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to check the database connection
        result = db.execute(text("SELECT 1"))
        if result.fetchone():
            return {
                "status": "success",
                "message": "Database connection is active.",
                "timestamp": str(datetime.now())
            }
        else:
            raise HTTPException(status_code=500, detail="Database connection check failed.")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
