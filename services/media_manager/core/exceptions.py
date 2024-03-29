class MediaFileNotFind(Exception):

    def __init__(self, link: str):
        super().__init__(
            f"Unable to receive media file from {link}"
        )


class UndefinedStateClient(Exception):

    def __init__(self, name: str):
        super().__init__(
            f"Undefined state client {name}"
        )


class UndefinedMessageBroker(Exception):

    def __init__(self, name: str):
        super().__init__(
            f"Undefined message broker {name}"
        )
