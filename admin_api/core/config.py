from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ADMIN_TOKEN: str
    REDIS_URL: str = "redis://127.0.0.1:6379/0"
    REDIS_PREFIX: str = "g"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    def get_key(self, module: str, sub: str = "") -> str:
        """Generate a Redis key following ``{PREFIX}:{module}:{sub}`` convention.

        When *sub* is omitted the key is ``{PREFIX}:{module}``.
        """
        prefix = self.REDIS_PREFIX
        if sub:
            return f"{prefix}:{module}:{sub}"
        return f"{prefix}:{module}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
