import os
from pathlib import Path
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
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
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        p = Path(target_file_path)
        if not p.is_file():
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if ".py" not in target_file_path or len(target_file_path.split(".py")) != 2:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        if args:
            command.extend(args)

        completed_process = subprocess.run(
            command,
            capture_output=True,
            timeout=30,
            text=True,
            cwd=working_directory_abs_path,
        )
        output = ""
        if completed_process.returncode != 0:
            output += f"Process exited with code {-1*completed_process.returncode}"

        if not completed_process.stderr and not completed_process.stdout:
            output += f"\nNo output produced"
        if completed_process.stdout:
            output += f"\nSTDOUT: {completed_process.stdout}"
        if completed_process.stderr:
            output += f"\nSTDERR: {completed_process.stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python script that exists relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The input arguments (if needed) for the python script",
            ),
        },
    ),
)
