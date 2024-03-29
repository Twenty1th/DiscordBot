from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self, Any

from services.media_manager.core.entities import Message
from services.media_manager.core.settings import Settings


class MessageBroker(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    async def connect(self) -> Self:
        ...

    @abstractmethod
    async def disconnect(self):
        ...

    @abstractmethod
    async def get(self) -> list[Message]:
        ...

    @abstractmethod
    async def confirm_msgs(self, msg: list[Any]):
        ...
