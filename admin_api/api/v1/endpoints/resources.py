from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, HttpUrl
from redis.asyncio import Redis

from core.config import Settings, get_settings
from core.redis import get_redis

router = APIRouter(tags=["resources"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class URLMapping(BaseModel):
    original_url: str = Field(max_length=2048)
    jump_id: str = Field(max_length=256)

    model_config = {"strict": True}


class BatchURLMappingRequest(BaseModel):
    mappings: list[URLMapping] = Field(min_length=1, max_length=500)

    model_config = {"strict": True}


class BatchURLMappingResponse(BaseModel):
    added: int


class StatsOverview(BaseModel):
    total_users: int
    total_urls: int


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _urls_key(settings: Settings) -> str:
    return settings.get_key("urls")


def _users_index_key(settings: Settings) -> str:
    return settings.get_key("users_index")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/urls/mapping", response_model=BatchURLMappingResponse)
async def create_url_mappings(
    body: BatchURLMappingRequest,
    rdb: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> BatchURLMappingResponse:
    """Batch-create shortened URL mappings into the ``{prefix}:urls`` hash."""
    urls_key = _urls_key(settings)
    mapping = {m.jump_id: m.original_url for m in body.mappings}
    await rdb.hset(urls_key, mapping=mapping)
    return BatchURLMappingResponse(added=len(mapping))


@router.get("/stats/overview", response_model=StatsOverview)
async def stats_overview(
    rdb: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> StatsOverview:
    """Return aggregate counts of users and URL mappings.

    Uses ``SCAN`` to count user keys (never ``KEYS *``).
    """
    # Count URLs – single HLEN call on the urls hash
    urls_key = _urls_key(settings)
    total_urls = await rdb.hlen(urls_key)

    # Count users via SCAN over user hash keys
    user_prefix = settings.get_key("user", "")
    total_users = 0
    cursor: int | None = 0
    while cursor:
        cursor, keys = await rdb.scan(cursor=cursor or 0, match=f"{user_prefix}*", count=200)
        total_users += len(keys)
        if cursor == 0:
            break

    return StatsOverview(total_users=total_users, total_urls=total_urls)
