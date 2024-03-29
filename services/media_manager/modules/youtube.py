from __future__ import annotations

import os
from pathlib import Path

from pytube import YouTube

from services.media_manager.core.entities import MediaFile
from services.media_manager.core.exceptions import MediaFileNotFind
from services.media_manager.core.settings import Settings
from services.media_manager.modules.base import ContentDownloader


class YTDownloader(ContentDownloader):

    def __init__(self, *, settings: Settings):
        self.settings = settings

    def download(self, link):
        yt = YouTube(link).streams.filter(
            file_extension=self.settings.source_file_ext,
            progressive=False,
            type='audio'
        )
        file = yt.first()
        if file is None:
            raise MediaFileNotFind(link)
        filename = "_".join(file.default_filename.lower().split(" "))
        path_to_file = f"{self.settings.path_to_download}/{filename}"
        if not Path(path_to_file).exists():
            print("Media file not exists. Downloading ...")
            file.download(
                output_path=self.settings.path_to_download,
                filename=filename
            )
            print(f"Media file downloaded {path_to_file}")
        return MediaFile(
            path=path_to_file,
            filename=filename,
            link=link
        )


