from fastapi import Depends, HTTPException, Request, status

from core.config import get_settings, Settings


async def verify_admin_token(
    request: Request, settings: Settings = Depends(get_settings)
) -> str:
    """Extract and validate ``Admin-Token`` from request headers."""
    token = request.headers.get("Admin-Token", "")
    if not token or token != settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing Admin-Token",
        )
    return token
