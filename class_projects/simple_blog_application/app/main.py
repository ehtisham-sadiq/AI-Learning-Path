from fastapi import FastAPI
from .routers import root, payment, auth

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

app.include_router(root.router)
app.include_router(auth.router)
app.include_router(payment.router)