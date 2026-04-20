import os
from pathlib import Path
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(
            os.path.join(working_directory_abs_path, file_path)
        )
        can_access = (
            os.path.commonpath([working_directory_abs_path, target_file_path])
            == working_directory_abs_path
        )
        if not can_access:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if "/" in file_path:
            dir_path = target_file_path.split("/")
            dir_path = "/".join(dir_path[: len(dir_path) - 1])
            os.makedirs(dir_path, exist_ok=True)

        p = Path(target_file_path)
        if p.is_dir():
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        with open(target_file_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write a file content that exists relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string content that needs to be written in the file",
            ),
        },
    ),
)
