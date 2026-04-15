from redis.asyncio import ConnectionPool, Redis

from core.config import get_settings

_pool: ConnectionPool | None = None


def _get_pool() -> ConnectionPool:
    global _pool
    if _pool is None:
        settings = get_settings()
        _pool = ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)
    return _pool


def get_redis() -> Redis:
    """Return an async Redis client backed by the shared connection pool."""
    return Redis(connection_pool=_get_pool())
