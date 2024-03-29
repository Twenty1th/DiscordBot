from services.media_manager.core.entities import StateStatus
from services.media_manager.core.settings import Settings
from services.media_manager.state_client.base import StateClient


class StateManager:

    def __init__(self, settings: Settings, state_client: StateClient):
        self.setting = settings
        self.state_client = state_client

    async def set_status(self, key: str, status: StateStatus):
        await self.state_client.set(
            key=key,
            status=status
        )

    async def get_status(self, key: str) -> StateStatus:
        return StateStatus[await self.state_client.get(key)]

