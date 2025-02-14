from fastapi import FastAPI


app = FastAPI(version="01", title="First App")

@app.get("/")
def root_user():
    return {"Hello": "Hello"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}