import os
from pathlib import Path


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        target_dir_is_valid = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not target_dir_is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        p = Path(directory)
        if not p.is_dir():
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        return f"Error: {e}"
