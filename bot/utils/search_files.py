import os

from .constants import DOWNLOADS_DIR


def check_if_user_directories_have_files(username: str) -> bool:
    for root, dirs, files in os.walk(DOWNLOADS_DIR):
        for dir_name in dirs:
            if dir_name.startswith(username):
                username_directory = os.path.join(root, dir_name)
                if any(
                    os.path.isfile(os.path.join(username_directory, filename))
                    for filename in os.listdir(username_directory)
                ):
                    return True
    return False
