from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env',
                                      env_file_encoding='utf-8')

    path_to_download: str
    source_file_ext: str

    state_client: str = "redis"

    msg_broker: str = "redis"
    msg_broker_channel: str = "media:{module_name}:music"

    workers_count: int = 4
