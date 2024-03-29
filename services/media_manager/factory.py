from __future__ import annotations

from functools import lru_cache

from services.media_manager.core.exceptions import UndefinedStateClient, \
    UndefinedMessageBroker
from services.media_manager.core.settings import Settings
from services.media_manager.modules.base import ContentDownloader
from services.media_manager.modules.youtube import YTDownloader
from services.media_manager.msg_broker.base import MessageBroker
from services.media_manager.msg_broker.redis import RedisMessageBroker
from services.media_manager.state_client.base import StateClient
from services.media_manager.state_client.redis import RedisStateClient
from services.media_manager.state_manager.manager import StateManager
from services.media_manager.worker import MediaWorker


class ServiceFactory:

    @staticmethod
    @lru_cache(256)
    def get_settings() -> Settings:
        s = Settings()
        return s

    @staticmethod
    def create_state_client(settings: Settings) -> StateClient:
        match settings.state_client:
            case "redis":
                return RedisStateClient(settings=settings)
            case _:
                raise UndefinedStateClient(settings.state_client)

    @staticmethod
    def create_state_manager(settings: Settings,
                             state_client: StateClient) -> StateManager:
        return StateManager(settings=settings, state_client=state_client)

    @staticmethod
    def create_downloader_service(settings: Settings) -> ContentDownloader:
        return YTDownloader(settings=settings)

    @staticmethod
    def create_message_broker(settings: Settings) -> MessageBroker:
        match settings.msg_broker:
            case "redis":
                return RedisMessageBroker(settings=settings)
            case _:
                raise UndefinedMessageBroker(settings.msg_broker)

    @staticmethod
    def create_main_worker(
            *,
            settings: Settings,
            downloader: ContentDownloader,
            state_manager: StateManager,
            message_broker: MessageBroker
    ):
        return MediaWorker(
            settings=settings,
            state_manager=state_manager,
            downloader=downloader,
            message_broker=message_broker
        )
