from fastapi import APIRouter

router = APIRouter(
    tags=["Root"]
)

@router.get("/")
def root():
    return {"message": "Welcome to Fastapi applictaion"}

@router.get("/about")
def about():
    return {"message": "Welcome to About page"}