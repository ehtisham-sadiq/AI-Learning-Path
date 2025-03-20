from fastapi import APIRouter

router = APIRouter(
    tags=["Payment"]
)

@router.get("/payments")
def payments():
    return {"message": "Welcome to Payments page"}

# get payments of a user by its name
@router.get("/payments/{name}")
def payments(name: str):
    return {"message": f"Welcome to Payments page of {name}"}
