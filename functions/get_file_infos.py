import os
from pathlib import Path
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        target_dir_is_valid = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not target_dir_is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        p = Path(target_dir)
        if not p.is_dir():
            return f'Error: "{directory}" is not a directory'

        target_dir_content = ""
        for entry in os.listdir(target_dir):
            full_path = os.path.join(target_dir, entry)
            stats = os.stat(full_path)
            p = Path(full_path)
            target_dir_content += (
                f"- {entry}: file_size={stats.st_size} bytes, is_dir={p.is_dir()}\n"
            )
        return target_dir_content
    except Exception as e:
        # print(e)
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
