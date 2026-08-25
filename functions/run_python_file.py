import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.normpath(os.path.commonpath([working_dir_abs, target_file])) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_file]
            if args:
                command.extend(args)
            completed_command = subprocess.run(command, cwd=working_dir_abs, capture_output=True, timeout=30, text=True)
            output_str = ""
            if completed_command.returncode:
                output_str += "Process exited with code X"
            if completed_command.stdout == "" and completed_command.stderr == "":
                output_str += "No output produced"
            else:
                output_str += f"STDOUT: {completed_command.stdout}"
                output_str += f"STDERR: {completed_command.stderr}"
            return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file in the specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "required": ["file_path"],
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "list[str]",
                    "description": "List of additional arguments to pass to the Python file",
                },
            },
        },
    },
}
