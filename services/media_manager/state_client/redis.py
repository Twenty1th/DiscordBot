from __future__ import annotations

from typing import Optional

import redis.asyncio as async_redis

from .base import StateClient
from ..core.entities import StateStatus


class RedisStateClient(StateClient):
    _client: async_redis

    async def connect(self):
        self._client = async_redis.Redis()
        print(f"Redis Ping successful: {await self._client.ping()}")
        return self

    async def get(self, key: str):
        status: Optional[bytes] = await self._client.get(key)
        if status is not None:
            return StateStatus[status.decode("utf-8")]
        return StateStatus.NotFound

    async def set(self, key, status: str):
        await self._client.set(
            name=key,
            value=status
        )

    async def disconnect(self):
        await self._client.aclose()
