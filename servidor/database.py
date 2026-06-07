import redis
from config import settings

class CacheService:
    def __init__(self):
        self._client = redis.Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            decode_responses=True
        )
    # limpa o cache automaticamente depois de 24 horas o status da geração do certificado (task_id)
    def set_status(self, task_id: str, status: str, ttl: int = 86400) -> None:
        self._client.set(task_id, status, ttl)

    def get_status(self, task_id: str) -> str:
            return self._client.get(task_id)