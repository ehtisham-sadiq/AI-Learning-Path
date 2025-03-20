```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI entry point (app setup, router inclusion)
│   ├── models.py                # SQLAlchemy models (User, Page)
│   ├── schemas.py               # Pydantic schemas (request/response validation)
│   ├── database.py              # Database connection setup (PostgreSQL engine/session)
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py            # Authentication routes (login, token handling)
│   │   └── helpers.py           # Password hashing, JWT creation/verification
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── routes.py            # CRUD endpoints for pages
│   │   └── services.py          # Business logic for creating/updating/deleting pages
│   ├── users/
│   │   ├── __init__.py
│   │   ├── routes.py            # Admin endpoints (create/list/delete users)
│   │   └── services.py          # Business logic for user management
│   └── config.py                # Configuration settings (DB URL, JWT secrets, etc.)
├── requirements.txt             # Python dependencies
├── Dockerfile                   # (Optional) Containerize the application
└── README.md                    # Basic setup and local dev instructions
```

```
FROM python:3.10.4

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```