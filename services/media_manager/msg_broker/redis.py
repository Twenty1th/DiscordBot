import asyncio

import redis as _redis
import redis.asyncio as async_redis

from .base import MessageBroker
from ..core.entities import Message, MessageData

type StreamName = bytes
type StreamMsgID = bytes
type StreamMsgData = dict[bytes, bytes]
type StreamMsgs = tuple[StreamMsgID, StreamMsgData]
type Msg = tuple[StreamName, list[StreamMsgs]]


class RedisMessageBroker(MessageBroker):
    _DEFAULT_READ_ITEMS = 10

    _client: async_redis

    async def connect(self):
        self._client = async_redis.Redis()
        print(f"Redis Ping successful: {await self._client.ping()}")
        await self._create_stream_group()
        return self

    async def _create_stream_group(self):
        try:
            await self._client.xgroup_create(
                self.settings.msg_broker_channel.format(module_name="youtube"),
                "youtube",
                0,
                mkstream=True
            )
        except _redis.exceptions.ResponseError:
            print("Consumer group already created")
            return

        except Exception as e:
            print(e)
            raise

    async def get(self, count: int = _DEFAULT_READ_ITEMS):
        res = await self._read_msgs()
        msgs = []
        for stream_msg in res:
            _msg = Message(
                id=stream_msg[0].decode("utf-8"),
                data=MessageData.model_validate(
                    {key.decode("utf-8"): value.decode("utf-8")
                     for key, value in stream_msg[1].items()}))
            msgs.append(_msg)
        return msgs

    def _filter_not_empty_res(self, res: list[Msg]):
        not_empty_msgs = []
        for stream in res:
            not_empty_msgs.extend(
                list(filter(lambda x: x[1], stream[1]))
            )
        return not_empty_msgs

    async def _read_msgs(self) -> list[StreamMsgs]:
        res = await self._read_pending_msgs()
        if not res:
            res = await self._read_new_msgs()
        return res

    async def _read_pending_msgs(self) -> list[StreamMsgs]:
        streams = {
            self.settings.msg_broker_channel.format(module_name="youtube"): "0"
        }
        res: list[Msg] = await self._client.xreadgroup(
            streams=streams,
            consumername=asyncio.current_task().get_name(),
            groupname="youtube",
            count=self._DEFAULT_READ_ITEMS,
        )
        return self._filter_not_empty_res(res)

    async def _read_new_msgs(self) -> list[StreamMsgs]:
        streams = {
            self.settings.msg_broker_channel.format(module_name="youtube"): ">"
        }
        res: list[Msg] = await self._client.xreadgroup(
            streams=streams,
            consumername=asyncio.current_task().get_name(),
            groupname="youtube",
            count=self._DEFAULT_READ_ITEMS,
        )
        return self._filter_not_empty_res(res)

    async def confirm_msgs(self, msgs: list[Message]):
        stream_name = self.settings.msg_broker_channel.format(
            module_name="youtube")
        stream_msgs_ids = [msg.id for msg in msgs]
        await self._client.xdel(
            stream_name,
            *stream_msgs_ids
        )
        print(
            f"Messages {', '.join(stream_msgs_ids)} successfully confirmed and removed")

    async def disconnect(self):
        await self._client.aclose()
