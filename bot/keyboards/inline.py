from typing import List
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..types import ZipperOption, ZipperOptionString


class ZipperCallback(CallbackData, prefix="zipper"):
    option: ZipperOptionString
    username: str


class ClearBufferKeyboard(InlineKeyboardBuilder):
    def __init__(self, username: str) -> None:
        super().__init__()
        self.button(
            text="Clear buffer",
            callback_data=ZipperCallback(option=ZipperOption.CLEAR, username=username),
        )
        self.adjust(1)


class ZipperKeyboard(InlineKeyboardBuilder):
    def __init__(self, username: str, sizes: List[int]) -> None:
        super().__init__()
        self.button(
            text="Zip files from buffer",
            callback_data=ZipperCallback(option=ZipperOption.SAVE, username=username),
        )
        self.button(
            text="Open buffer",
            callback_data=ZipperCallback(option=ZipperOption.OPEN, username=username),
        )
        self.button(
            text="Close buffer",
            callback_data=ZipperCallback(option=ZipperOption.CLOSE, username=username),
        )
        self.attach(ClearBufferKeyboard(username))
        self.adjust(*sizes)
