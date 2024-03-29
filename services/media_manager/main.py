import asyncio

from services.media_manager.factory import ServiceFactory


async def main():
    settings = ServiceFactory.get_settings()

    state_client = ServiceFactory.create_state_client(settings)
    await state_client.connect()

    state_manager = ServiceFactory.create_state_manager(settings, state_client)

    downloader = ServiceFactory.create_downloader_service(settings)

    message_broker = ServiceFactory.create_message_broker(settings)
    await message_broker.connect()

    worker = ServiceFactory.create_main_worker(
        settings=settings,
        downloader=downloader,
        state_manager=state_manager,
        message_broker=message_broker
    )
    await worker.start()


if __name__ == '__main__':
    asyncio.run(main())
