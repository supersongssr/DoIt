import secrets
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from redis.asyncio import Redis

from core.config import Settings, get_settings
from core.redis import get_redis

router = APIRouter(tags=["users"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class BatchRegisterRequest(BaseModel):
    n: int = Field(ge=1, le=1000, description="Number of accounts to create")

    model_config = {"strict": True}


class BatchRegisterResponse(BaseModel):
    created: int
    accounts: list[dict[str, str]]


class UserUpdateRequest(BaseModel):
    name: str | None = Field(default=None, max_length=128)
    pwd: str | None = Field(default=None, max_length=256)
    coins: int | None = Field(default=None, ge=0)

    model_config = {"strict": True}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _user_key(email: str, settings: Settings) -> str:
    return settings.get_key("user", email)


def _users_index_key(settings: Settings) -> str:
    return settings.get_key("users_index")


def _user_count_key(settings: Settings) -> str:
    return settings.get_key("all_users_count")


def _generate_credential(length: int = 16) -> str:
    """Generate a cryptographically strong hex string."""
    return secrets.token_hex(length)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/batch-register", response_model=BatchRegisterResponse)
async def batch_register(
    body: BatchRegisterRequest,
    rdb: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> BatchRegisterResponse:
    """Create *n* accounts with random email/password credentials."""
    accounts: list[dict[str, str]] = []
    index_key = _users_index_key(settings)
    count_key = _user_count_key(settings)

    for _ in range(body.n):
        email = f"{_generate_credential(8)}@batch"
        pwd = _generate_credential(8)
        user_id = await rdb.incr(count_key)

        user_key = _user_key(email, settings)
        user_data: dict[str, Any] = {
            "id": str(user_id),
            "name": email,
            "email": email,
            "pwd": pwd,
            "coins": "10",
            "urlclicks": "0",
            "devices": "0",
            "invites": "0",
            "inviteby": "",
        }
        await rdb.hset(user_key, mapping=user_data)
        await rdb.sadd(index_key, email)
        accounts.append({"email": email, "pwd": pwd})

    return BatchRegisterResponse(created=len(accounts), accounts=accounts)


@router.get("/users/{user_id}")
async def get_user_by_id(
    user_id: str,
    rdb: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> dict[str, Any]:
    """Look up a user by their numeric ID.

    Scans ``{prefix}:user_*`` hashes to find the matching ``id`` field.
    """
    cursor: int | None = 0
    prefix = settings.get_key("user", "")
    while cursor:
        cursor, keys = await rdb.scan(cursor=cursor or 0, match=f"{prefix}*", count=200)
        for key in keys:
            stored_id = await rdb.hget(key, "id")
            if stored_id == user_id:
                data = await rdb.hgetall(key)
                return data
        if cursor == 0:
            break

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    body: UserUpdateRequest,
    rdb: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    """Update mutable fields on a user identified by numeric ID."""
    user_key = None
    prefix = settings.get_key("user", "")
    cursor: int | None = 0
    while cursor:
        cursor, keys = await rdb.scan(cursor=cursor or 0, match=f"{prefix}*", count=200)
        for key in keys:
            stored_id = await rdb.hget(key, "id")
            if stored_id == user_id:
                user_key = key
                break
        if user_key or cursor == 0:
            break

    if user_key is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    updates: dict[str, str] = {}
    if body.name is not None:
        updates["name"] = body.name
    if body.pwd is not None:
        updates["pwd"] = body.pwd
    if body.coins is not None:
        updates["coins"] = str(body.coins)

    if updates:
        await rdb.hset(user_key, mapping=updates)

    return {"status": "updated", **updates}
