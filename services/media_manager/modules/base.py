from abc import ABC, abstractmethod

from services.media_manager.core.entities import MediaFile


class ContentDownloader(ABC):

    @abstractmethod
    def download(self, link: str) -> MediaFile: ...
