from enum import Enum
from typing import Type, Literal

from .utils import DocumentDownloader, PhotoDownloader


class ZipperOption(str, Enum):
    SAVE = "save"
    OPEN = "open"
    CLOSE = "close"
    CLEAR = "clear"


ZipperOptionString: Type = Literal[
    ZipperOption.SAVE, ZipperOption.OPEN, ZipperOption.CLOSE, ZipperOption.CLEAR
]


class DownloaderOption(str, Enum):
    DOCUMENT = "document"
    PHOTO = "photo"


DownloaderOptionString: Type = Literal[
    DownloaderOption.DOCUMENT, DownloaderOption.PHOTO
]
