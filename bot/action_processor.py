import math
import os
import zipfile
import telepot
from datetime import datetime
from enum import Enum
from shutil import rmtree
from contextlib import suppress
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, Message
from .config import BOT, SAVE_DIR_NAME, IMAGES_DIR_NAME, DOCS_DIR_NAME


class ContentType(Enum):
    PHOTO = "photo"
    DOCUMENT = "document"
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    ANY = "any"


class ActionProcessor:
    BASE_IMAGES_PATH = os.path.join(SAVE_DIR_NAME, IMAGES_DIR_NAME)
    BASE_DOCS_PATH = os.path.join(SAVE_DIR_NAME, DOCS_DIR_NAME)
    BUFFER_LIMIT = 20
    BYTE_TO_MEGABYTE = 1024 ** 2

    def __init__(self):
        self.content_type_actions = {
            ContentType.PHOTO: self.handle_photo,
            ContentType.DOCUMENT: self.handle_document,
            ContentType.VIDEO: self.handle_document,
            ContentType.AUDIO: self.handle_document,
            ContentType.TEXT: self.handle_text,
        }

    def on_chat_message(self, msg: Message) -> None:
        content_type, chat_type, chat_id = telepot.glance(msg)
        username = msg["from"]["username"]
        with suppress(ValueError):
            converted_content_type = ContentType.ANY
            converted_content_type = ContentType(content_type)
        path_to_save = self.BASE_IMAGES_PATH if converted_content_type == ContentType.PHOTO else self.BASE_DOCS_PATH
        user_files_dir = os.path.join(path_to_save, username)
        document_content_types = [
            cont_type for cont_type in self.content_type_actions if cont_type != ContentType.TEXT
        ]

        if not os.path.exists(user_files_dir) and converted_content_type in document_content_types:
            os.makedirs(user_files_dir)

        if converted_content_type in document_content_types:
            self.content_type_actions[converted_content_type](msg, user_files_dir, chat_id, content_type)
        elif converted_content_type == ContentType.TEXT:
            self.content_type_actions[converted_content_type](msg, username, chat_id)
        else:
            self.handle_other_content(chat_id)

    def handle_photo(self, msg: Message, user_files_dir: str, chat_id: int, *args) -> None:
        photo_id = msg["photo"][-1]["file_id"]
        photo_data = BOT.getFile(photo_id)
        photo_ext = f".{photo_data['file_path'].split('.')[-1]}"
        save_photo_name = photo_data["file_id"] + photo_ext
        local_image_path = os.path.join(user_files_dir, save_photo_name)
        self.download_control(photo_id, local_image_path, chat_id)

    def handle_document(self, msg: Message, user_files_dir: str, chat_id: int, document_type: str) -> None:
        media_id = msg[document_type]["file_id"]
        media_name = msg[document_type]["file_name"]
        local_media_path = os.path.join(user_files_dir, media_name)
        self.download_control(media_id, local_media_path, chat_id)

    def handle_text(self, msg: Message, username: str, chat_id: int) -> None:
        if msg["text"] == "/zip":
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        self.create_button("Yes", "save", username),
                        self.create_button("Nope, clear the buffer", "discard", username),
                    ],
                ]
            )

            BOT.sendMessage(chat_id, "Zip files from buffer?", reply_markup=keyboard)
        else:
            BOT.sendMessage(
                chat_id,
                "Send me the files and I'll zip them for you. Type /zip after the files are uploaded.",
            )

    def handle_other_content(self, chat_id: int) -> None:
        BOT.sendMessage(
            chat_id,
            "Send me the files and I'll zip them for you. Type /zip after the files are uploaded.",
        )

    def on_callback_query(self, msg: Message) -> None:
        query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
        action, username = query_data.split()[0], query_data.split()[1]

        if not self.is_buffer_filled(username):
            BOT.answerCallbackQuery(query_id, "Buffer is empty. Send files to fill it.")
            return None

        images_path = os.path.join(os.getcwd(), self.BASE_IMAGES_PATH, username)
        files_path = os.path.join(os.getcwd(), self.BASE_DOCS_PATH, username)
        zip_name = f"{username}.zip"

        if action == "save":
            self.rename_files_with_modified_time(images_path)
            zipf = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
            self.zipdir(os.path.join(self.BASE_IMAGES_PATH, username), zipf, IMAGES_DIR_NAME)
            self.zipdir(os.path.join(self.BASE_DOCS_PATH, username), zipf, DOCS_DIR_NAME)
            zipf.close()
            message = self.buffer_control(
                self.get_folder_content_size(files_path),
                self.get_folder_content_size(images_path),
                images_path=images_path,
                files_path=files_path,
            )
            try:
                BOT.sendDocument(from_id, open(zip_name, "rb"))
                BOT.answerCallbackQuery(query_id, message)
            except telepot.exception.TelegramError:
                BOT.answerCallbackQuery(
                    query_id,
                    "Zip file size is above 50MB! Buffer cleared automatically.",
                )
            os.remove(zip_name)
        else:
            removed_images_number = self.clear_path(images_path)
            removed_files_number = self.clear_path(files_path)
            BOT.answerCallbackQuery(
                query_id,
                self.generate_removal_message(removed_images_number, removed_files_number),
            )

    def is_buffer_filled(self, username: str) -> bool:
        is_images_buffer_filled = os.path.exists(
            os.path.join(self.BASE_IMAGES_PATH, username)
        )
        is_docs_buffer_filled = os.path.exists(
            os.path.join(self.BASE_DOCS_PATH, username)
        )
        return is_images_buffer_filled or is_docs_buffer_filled

    def download_control(self, file_id: str, dest: str, chat_id: int) -> None:
        try:
            BOT.download_file(file_id, dest)
        except telepot.exception.TelegramError:
            BOT.sendMessage(
                chat_id,
                "File too large! Unable to download. Please try to send a smaller one.",
            )

    def zipdir(self, path: str, ziph: zipfile.ZipFile, files_type: str) -> None:
        abs_src = os.path.abspath(path)
        for root, dirs, files in os.walk(path):
            for file in files:
                abs_file_path = os.path.abspath(os.path.join(root, file))
                end_path = os.path.join(files_type, abs_file_path[len(abs_src) + 1:])
                ziph.write(abs_file_path, end_path)

    def rename_files_with_modified_time(self, path: str) -> None:
        for root, dirs, files in os.walk(path):
            for filename in files:
                modified_time = os.path.getmtime(os.path.join(path, filename))
                formatted_time = datetime.fromtimestamp(modified_time).strftime("image_%Y-%m-%d_%H-%M-%S_%f")[:-3]
                file_ext = filename.split(".")[-1]
                new_name = f"{formatted_time}.{file_ext}"
                os.rename(
                    os.path.join(path, filename),
                    os.path.join(path, new_name),
                )

    def create_button(self, text: str, user_option: str, username: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=text,
            callback_data=user_option + " " + username,
        )

    def clear_path(self, path: str) -> int:
        remove_files_number = 0
        if os.path.exists(path):
            remove_files_number = sum(
                1 for root, dirs, files in os.walk(path) for _ in files
            )
            with suppress(OSError):
                rmtree(path)
        return remove_files_number

    def generate_removal_message(self, removed_images: int, removed_files: int) -> str:
        messages = {
            "image": removed_images,
            "file": removed_files,
        }

        message_parts = [
            f"{messages[key]} {key}{'s' if messages[key] > 1 else ''}"
            for key in messages
            if messages[key] > 0
        ]

        if message_parts:
            return " and ".join(message_parts) + " removed from buffer!"
        else:
            return "Nothing to remove from the buffer."

    def get_folder_content_size(self, path: str) -> float:
        size = 0
        if not os.path.exists(path):
            return size

        for element in os.scandir(path):
            size += os.path.getsize(element)

        return size / self.BYTE_TO_MEGABYTE

    def buffer_control(self, *disk_usage, images_path: str, files_path: str) -> str:
        default_message_part = "Here is your archive!"
        if math.ceil(sum(disk_usage)) >= self.BUFFER_LIMIT:
            self.clear_path(files_path)
            self.clear_path(images_path)
            return f"{default_message_part}\nBuffer is cleared automatically because your zip is too large!"
        return default_message_part
