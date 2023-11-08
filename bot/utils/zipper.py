import os
import zipfile
from .constants import DOWNLOADS_DIR


def zipdir(zipf: zipfile.ZipFile, username: str) -> None:
    abs_root_path = os.path.abspath(DOWNLOADS_DIR)
    for root, dirs, files in os.walk(DOWNLOADS_DIR):
        for file in files:
            abs_file_path = os.path.abspath(os.path.join(root, file))
            abs_dir_path = os.path.dirname(abs_file_path)
            if abs_dir_path.endswith(username):
                zip_file_path = abs_file_path[len(abs_root_path):]
                zip_path_list = os.path.split(zip_file_path)
                result_zip_file_path = os.path.join(zip_path_list[0].removesuffix(username), zip_path_list[1])
                zipf.write(abs_file_path, result_zip_file_path)
