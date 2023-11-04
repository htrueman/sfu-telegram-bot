import os
import zipfile
import telepot
from shutil import rmtree
from contextlib import suppress
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, Message
from .config import BOT, SAVE_DIR_NAME, IMAGES_DIR_NAME, DOCS_DIR_NAME


def zipdir(path: str, ziph: zipfile.ZipFile, files_type: str) -> None:
    abs_src = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            abs_file_path = os.path.abspath(os.path.join(root, file))
            end_path = os.path.join(files_type, abs_file_path[len(abs_src) + 1:])
            ziph.write(abs_file_path, end_path)


def rename_files_with_modified_time(path: str) -> None:
    for root, dirs, files in os.walk(path):
        for filename in files:
            modified_time = os.path.getmtime(os.path.join(path, filename))
            file_ext = filename.split(".")[-1]
            new_name = (
                    str(modified_time).split(".")[0] + str(modified_time).split(".")[1]
            )
            os.rename(
                os.path.join(path, filename),
                os.path.join(path, new_name + "." + file_ext),
            )


def create_button(text: str, user_option: str, username: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=user_option + " " + username,
    )


def clear_path(path: str) -> None:
    if os.path.exists(path):
        with suppress(OSError):
            rmtree(path)


class ActionProcessor:
    BASE_IMAGES_PATH = os.path.join(SAVE_DIR_NAME, IMAGES_DIR_NAME)
    BASE_DOCS_PATH = os.path.join(SAVE_DIR_NAME, DOCS_DIR_NAME)

    def on_chat_message(self, msg: Message) -> None:
        content_type, chat_type, chat_id = telepot.glance(msg)
        username = msg["from"]["username"]

        if content_type in ["photo", "document"]:
            path_to_save = self.BASE_IMAGES_PATH if content_type == "photo" else self.BASE_DOCS_PATH
            user_files_dir = os.path.join(path_to_save, username)
            if not os.path.exists(user_files_dir):
                os.makedirs(user_files_dir)

            if content_type == "photo":
                photo_id = msg["photo"][-1]["file_id"]
                photo_data = BOT.getFile(photo_id)
                save_photo_name = photo_data["file_id"] + "." + photo_data["file_path"].split(".")[-1]
                local_image_path = os.path.join(user_files_dir, save_photo_name)
                BOT.download_file(photo_id, local_image_path)
            elif content_type == "document":
                document_id = msg["document"]["file_id"]
                document_name = msg["document"]["file_name"]
                local_document_path = os.path.join(user_files_dir, document_name)
                BOT.download_file(document_id, local_document_path)
        elif content_type == "text" and msg["text"] == "/zip":
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        create_button("Yes", "save", username),
                        create_button("Nope, clear the buffer", "discard", username),
                    ],
                ]
            )

            BOT.sendMessage(chat_id, "Zip and save files from buffer?", reply_markup=keyboard)
        else:
            BOT.sendMessage(
                chat_id,
                "Send me the files and I'll zip them for you. Type /zip after the files are uploaded.",
            )

    def on_callback_query(self, msg: Message) -> None:
        query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
        if not self.is_buffer_filled(msg["from"]["username"]):
            BOT.answerCallbackQuery(query_id, "Buffer is empty. Send files to fill it.")
            return None

        action, username = query_data.split()[0], query_data.split()[1]

        images_path = os.path.join(os.getcwd(), self.BASE_IMAGES_PATH, username)
        files_path = os.path.join(os.getcwd(), self.BASE_DOCS_PATH, username)
        zip_name = f"{username}.zip"

        if action == "save":
            rename_files_with_modified_time(images_path)
            zipf = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
            zipdir(os.path.join(self.BASE_IMAGES_PATH, username), zipf, IMAGES_DIR_NAME)
            zipdir(os.path.join(self.BASE_DOCS_PATH, username), zipf, DOCS_DIR_NAME)
            zipf.close()
            BOT.sendDocument(from_id, open(zip_name, "rb"))
            os.remove(zip_name)
            BOT.answerCallbackQuery(query_id, text="Here is your archive.\nBuffer cleared!")
        elif action == "discard":
            BOT.answerCallbackQuery(query_id, text="Buffer cleared successfully!")

        clear_path(images_path)
        clear_path(files_path)

    def is_buffer_filled(self, username: str) -> bool:
        is_images_buffer_filled = os.path.exists(os.path.join(self.BASE_IMAGES_PATH, username))
        is_docs_buffer_filled = os.path.exists(os.path.join(self.BASE_DOCS_PATH, username))
        return is_images_buffer_filled or is_docs_buffer_filled
