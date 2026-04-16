import os
from pathlib import Path


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

        return target_file_path
    except Exception as e:
        return f"Error: {e}"
