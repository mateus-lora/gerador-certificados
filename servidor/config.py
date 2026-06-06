import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    EMAIL_REMETENTE: str
    SENHA_REMETENTE: str
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_QUEUE: str = "fila_certificados"
    
    BASE_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()