from enum import Enum
from typing import Type, Literal


class ZipperOption(str, Enum):
    SAVE = "save"
    OPEN = "open"
    CLOSE = "close"
    CLEAR = "clear"


ZipperOptionString: Type = Literal[
    ZipperOption.SAVE, ZipperOption.OPEN, ZipperOption.CLOSE, ZipperOption.CLEAR
]
