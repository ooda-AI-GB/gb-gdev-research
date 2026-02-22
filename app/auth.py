import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Token", auto_error=True)


def get_api_key(api_key: str = Security(api_key_header)) -> str:
    expected = os.getenv("GDEV_API_TOKEN", "dev-token")
    if api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
    return api_key
