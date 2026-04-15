import os

from fastapi import Depends, FastAPI

from api.deps import verify_admin_token
from api.v1.endpoints import users, resources
from core.config import get_settings

app = FastAPI(
    title="DoIt Admin API",
    version="0.1.0",
    dependencies=[Depends(verify_admin_token)],
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(resources.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}


def main() -> None:
    """Entry-point with systemd socket-activation support."""
    import uvicorn

    settings = get_settings()

    listen_fds = os.getenv("LISTEN_FDS")
    if listen_fds and int(listen_fds) >= 1:
        # systemd socket activation – fd 3 is the first passed socket (SD_LISTEN_FDS_START)
        uvicorn.run(
            "main:app",
            fd=3,
            log_level="info",
            factory=False,
        )
    else:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            log_level="info",
        )


if __name__ == "__main__":
    main()
