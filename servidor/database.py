import redis
from config import settings

class CacheService:
    def __init__(self):
        self._client = redis.Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            decode_responses=True
        )

    def set_status(self, task_id: str, status: str) -> None:
        self._client.set(task_id, status)

    def get_status(self, task_id: str) -> str:
        return self._client.get(task_id)