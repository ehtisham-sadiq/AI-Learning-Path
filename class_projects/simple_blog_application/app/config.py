# from pydantic import BaseSettings
from pydantic_settings import BaseSettings # NEW


class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "password"
    database_name: str = "blog_db"
    database_username: str = "postgres"
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    development_env: str = "prod"
    version: str = "1.0.0"

    class Config:
        env_file = ".env"
        
settings = Settings()