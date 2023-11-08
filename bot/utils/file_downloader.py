import os
from abc import ABC, abstractmethod
from typing import Optional, Any
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InlineKeyboardMarkup

from .constants import DOWNLOADS_DIR, MAX_BUFFER_SIZE_BS, MAX_DOWNLOAD_FILE_SIZE_MB


class BaseDownloader(ABC):
    filename_counters = {}

    def __init__(
        self,
        message: Message,
        clear_keyboard: InlineKeyboardMarkup,
        file_type: Optional[ContentType] = None,
        allow_duplicate_files: Optional[bool] = True,
    ) -> None:
        self.message = message
        self.keyboard = clear_keyboard
        self.file_type = file_type
        self.download_path = os.path.join(
            DOWNLOADS_DIR, file_type, message.from_user.username
        )
        self.is_duplicate_allowed = allow_duplicate_files
        self.create_user_dir(self.download_path)

    async def download_controller(
        self, file_id: str, local_file_path: str, file_size: int
    ) -> None:
        current_size = self.get_folder_content_size(self.download_path)
        future_size = current_size + file_size
        if future_size >= MAX_BUFFER_SIZE_BS or MAX_BUFFER_SIZE_BS - current_size <= 0:
            await self.message.bot.send_message(
                chat_id=self.message.chat.id,
                text=f"Could not be loaded to buffer!\n"
                f"The maximum size is {MAX_BUFFER_SIZE_BS // (1024 ** 2)} MB.\n"
                f"{(MAX_BUFFER_SIZE_BS - current_size) / (1024 ** 2):.2f} MB available.",
                reply_to_message_id=self.message.message_id,
                reply_markup=self.keyboard
            )
        else:
            local_file_path = self._process_duplicate_file(local_file_path)
            await self._big_files_handler(file_id, local_file_path)

    async def _big_files_handler(self, file_id: str, dst: str) -> None:
        try:
            await self.message.bot.download(file=file_id, destination=dst)
        except TelegramBadRequest:
            await self.message.bot.send_message(
                chat_id=self.message.chat.id,
                text=f"File is to big! Must be less than {MAX_DOWNLOAD_FILE_SIZE_MB} MB.",
                reply_to_message_id=self.message.message_id,
            )

    def _process_duplicate_file(self, local_file_path: str) -> str:
        if self.is_duplicate_allowed:
            new_filename = self._get_unique_filename(local_file_path)
            stored_filename = new_filename.split(".")[0].split("(")[0]
            if self.filename_counters[stored_filename] == 1:
                new_filename = self._get_unique_filename_from_local_dir(local_file_path)
            return os.path.join(os.path.dirname(local_file_path), new_filename)
        return local_file_path

    def _get_unique_filename(self, local_file_path: str) -> str:
        local_filename = os.path.basename(local_file_path)
        base, extension = os.path.splitext(local_filename)

        if base not in self.filename_counters:
            self.filename_counters[base] = 0

        counter = self.filename_counters[base]
        new_filename = (
            local_filename if counter == 0 else f"{base}({counter}){extension}"
        )

        self.filename_counters[base] += 1

        return new_filename

    def _get_unique_filename_from_local_dir(self, local_file_path: str) -> str:
        local_dir_path = os.path.dirname(local_file_path)
        local_filename = os.path.basename(local_file_path)
        base, extension = os.path.splitext(local_filename)

        existing_files = set(os.listdir(local_dir_path))
        counter = 0

        while local_filename in existing_files:
            counter += 1
            new_filename = f"{base}({counter}){extension}"
            local_filename = new_filename

        self.filename_counters[base] = counter + 1
        return local_filename

    def _set_time_name(self, current_filename: str) -> str:
        message_time = self.message.date.strftime(
            f"{self.file_type.value}_%Y-%m-%d_%H-%M-%S"
        )
        file_ext = current_filename.split(".")[-1]
        new_name = f"{message_time}.{file_ext}"
        return new_name

    @staticmethod
    def get_folder_content_size(path: str) -> float:
        size = 0
        if not os.path.exists(path):
            return size

        for element in os.scandir(path):
            size += os.path.getsize(element)

        return size

    @staticmethod
    def create_user_dir(path: str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)

    @abstractmethod
    async def download(self, *args) -> None:
        raise NotImplementedError


class DocumentDownloader(BaseDownloader):
    async def download(self) -> None:
        file_data = getattr(self.message, self.message.content_type)
        file_id = file_data.file_id
        filename = self._get_filename(file_data)
        file_size = file_data.file_size
        local_file_path = os.path.join(self.download_path, filename)
        await self.download_controller(file_id, local_file_path, file_size)

    def _get_filename(self, file_data: Any) -> str:
        try:
            filename = file_data.file_name
        except AttributeError:
            if hasattr(file_data, "mime_type"):
                file_ext = f".{os.path.split(file_data.mime_type)[-1]}"
            else:
                file_ext = ".mp4"
            filename = file_data.file_id + file_ext
            filename = self._set_time_name(filename)

        return filename


class PhotoDownloader(BaseDownloader):
    async def download(self) -> None:
        photo_id = self.message.photo[-1].file_id
        photo_data = await self.message.bot.get_file(photo_id)
        photo_ext = f".{photo_data.file_path.split('.')[-1]}"
        photo_name = f"{photo_data.file_id}.{photo_ext}"
        photo_name = self._set_time_name(photo_name)
        photo_size = photo_data.file_size
        local_photo_path = os.path.join(self.download_path, photo_name)
        await self.download_controller(photo_id, local_photo_path, photo_size)
