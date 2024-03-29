from abc import ABC, abstractmethod
from typing import Self, Optional

from services.media_manager.core.entities import StateStatus
from services.media_manager.core.settings import Settings


class StateClient(ABC):

    def __init__(self, settings: Settings):
        self.setting = settings

    @abstractmethod
    async def connect(self) -> Self:
        ...

    @abstractmethod
    async def get(self, key: str) -> StateStatus:
        ...

    @abstractmethod
    async def set(self, key, status: str):
        ...

    @abstractmethod
    async def disconnect(self): ...
