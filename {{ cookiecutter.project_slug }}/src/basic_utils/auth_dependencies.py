from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

import aiohttp
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from basic_utils.config import settings
from basic_utils.jwt_utils import decode_jwt
from basic_utils.redis_utils import get_redis_utils


PublicKeyGetter = Callable[[str | None], str | Awaitable[str]]

_bearer_scheme = HTTPBearer(auto_error=True)

async def get_public_key_from_text(_: str | None = None) -> str:
    """Возвращает публичный ключ из конфигурации."""
    return settings.jwt_public_key


async def get_public_key_from_server(key_id: str | None = None) -> str:
    """Возвращает публичный ключ через Redis-кэш и внешний сервис."""
    redis = get_redis_utils(prefix=settings.jwt_public_key_cache_prefix)
    cache_key = key_id or settings.jwt_default_key_id

    try:
        cached_key = await redis.get(cache_key)
        if cached_key:
            return cached_key

        timeout = aiohttp.ClientTimeout(total=settings.jwt_public_key_request_timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(settings.jwt_public_key_url) as response:
                response.raise_for_status()
                payload = await response.json()

        public_key = payload.get(settings.jwt_public_key_response_field)
        if not isinstance(public_key, str) or not public_key.strip():
            raise ValueError(
                "Public key is missing in JWT public key server response."
            )

        await redis.set(
            cache_key,
            public_key,
            ex=settings.jwt_public_key_cache_ttl,
        )
        return public_key
    finally:
        await redis.close()


def get_decoded_jwt_dependency(
    public_key_getter: PublicKeyGetter,
    *,
    algorithms: list[str] | None = None,
    audience: str | None = None,
    issuer: str | None = None,
    options: dict[str, Any] | None = None,
) -> Callable[..., Awaitable[dict[str, Any]]]:
    """Создает dependency, которая возвращает декодированный JWT."""

    async def _dependency(
        credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    ) -> dict[str, Any]:
        return await decode_jwt(
            credentials.credentials,
            public_key_getter,
            algorithms=algorithms,
            audience=audience,
            issuer=issuer,
            options=options,
        )

    return _dependency
