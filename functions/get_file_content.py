import os
from pathlib import Path
from config import MAX_ALLOWED_SIZE


def get_file_content(working_directory, file_path):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(
            os.path.join(working_directory_abs_path, file_path)
        )
        file_path_is_allowed = (
            os.path.commonpath([working_directory_abs_path, target_file_path])
            == working_directory_abs_path
        )
        if not file_path_is_allowed:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        f = Path(target_file_path)
        if not f.is_file():
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_content = ""
        with open(target_file_path, "r") as f:
            file_content = f.read(MAX_ALLOWED_SIZE)
            if f.read(1):
                file_content += f'[...File "{target_file_path}" truncated at {MAX_ALLOWED_SIZE} characters]'

        return file_content
    except Exception as e:
        return f"Error: {e}"
