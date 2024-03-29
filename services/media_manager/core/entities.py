from pydantic import BaseModel
from enum import StrEnum, unique


class MessageData(BaseModel):
    link: str
    resource: str


class Message(BaseModel):
    id: str
    data: MessageData


class MediaFile(BaseModel):
    path: str
    filename: str
    link: str


@unique
class StateStatus(StrEnum):
    Ok = "Ok"
    InProgress = "InProgress"
    Failed = "Failed"
    NotFound = "NotFound"
