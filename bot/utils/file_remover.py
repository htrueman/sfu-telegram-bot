import os
from contextlib import suppress
from shutil import rmtree
from typing import Dict
from .constants import DOWNLOADS_DIR


class FileRemover:
    def clear_root(self, username: str) -> Dict[str, int]:
        clear_statistics = {}
        upper_dirs = os.listdir(DOWNLOADS_DIR)
        for dir_name in upper_dirs:
            dir_path = os.path.join(DOWNLOADS_DIR, dir_name, username)
            clear_statistics[dir_name] = self._clear_path(dir_path)
        return clear_statistics

    @staticmethod
    def _clear_path(path: str) -> int:
        remove_files_number = 0
        if os.path.exists(path):
            remove_files_number = sum(
                1 for root, dirs, files in os.walk(path) for _ in files
            )
            with suppress(OSError):
                rmtree(path)
        return remove_files_number

    @staticmethod
    def generate_removal_message(messages: Dict[str, int]) -> str:
        message_parts = [
            f"{messages[key]} {key}{'s' if messages[key] > 1 else ''}"
            for key in messages
            if messages[key] > 0
        ]

        if message_parts:
            return (
                " , ".join(message_parts)
                + " removed from buffer!\nBuffer is empty now."
            )
        return "Nothing to remove from the buffer."
