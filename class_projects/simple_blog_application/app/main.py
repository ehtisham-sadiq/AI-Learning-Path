from marshal import version
from fastapi import FastAPI

title = "Simple Blog Application"
description = f"""
{title} helps you to do awesome things.
"""

app = FastAPI(
    title=title,
    description=description,
    version = "0.1.0",
    contact = {
        "name": "Ehtisham Sadiq",
        "email": "ehtisham.sadiq@leo-behe.com",
        "url": "https://github.com/ehtishamsadiq"
    }
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}






