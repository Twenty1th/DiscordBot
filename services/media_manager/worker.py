from __future__ import annotations

import asyncio
import typing
import time as t

from services.media_manager.core.entities import Message, StateStatus

if typing.TYPE_CHECKING:
    from services.media_manager.core.settings import Settings
    from services.media_manager.modules.base import ContentDownloader
    from services.media_manager.msg_broker.base import MessageBroker
    from services.media_manager.state_manager.manager import StateManager


class MediaWorker:

    def __init__(
            self,
            *,
            settings: Settings,
            downloader: ContentDownloader,
            state_manager: StateManager,
            message_broker: MessageBroker
    ):
        self.settings = settings
        self.downloader = downloader
        self.state_manager = state_manager
        self.message_broker = message_broker

    async def start(self):
        async with asyncio.TaskGroup() as group:
            for num in range(self.settings.workers_count):
                group.create_task(self._start(), name=f"Media-worker-{num}")
                print(f"[Media Worker-{num}]: started at {t.strftime('%X')}")
        print(f"[Media Workers] finished at {t.strftime('%X')}")

    async def _start(self):
        while True:
            msgs = await self.message_broker.get()
            for msg in msgs:
                await self._process_msg(msg)
            # await self.message_broker.confirm_msgs(msg)
            await asyncio.sleep(3)

    async def _process_msg(self, msg: Message):
        print(msg)
        msg_status = await self.state_manager.get_status(msg.id)
        match msg_status:
            case StateStatus.NotFound:
                await self.state_manager.set_status(
                    key=msg.id,
                    status=StateStatus.InProgress
                )
                await asyncio.to_thread(
                    self.downloader.download,
                    msg.data.link)
                await self.state_manager.set_status(
                    key=msg.id,
                    status=StateStatus.Ok
                )
                await self.message_broker.confirm_msgs([msg])

            case StateStatus.InProgress, StateStatus.Ok:
                print(
                    f"[{asyncio.current_task().get_name()}]: {msg.id} already in progress")  # noqa
                await self.message_broker.confirm_msgs([msg])

            case StateStatus.Failed:  # TODO
                ...
