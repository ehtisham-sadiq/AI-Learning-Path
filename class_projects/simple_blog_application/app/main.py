from fastapi import FastAPI
from .routers import root, payment, auth, post, user, vote, db_route

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
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(db_route.router)

