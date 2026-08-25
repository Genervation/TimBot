import os


def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = os.path.normpath(os.path.commonpath([working_dir_abs, target_file])) == working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot read {file_path} as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: {file_path}'
    else:
        MAX_CHARS = 10000

        with open(target_file, "r") as f:
            file_content_string = ""
            file_content_string += f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'\n[...File {file_path} truncated at {MAX_CHARS} characters]'
            return file_content_string

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Lists file content in a specified file path relative to the working directory, providing file content that may or may not be truncated and where it was truncated (if applicable)",
        "parameters": {
            "type": "object",
            "properties": {
                "required": ["file_path"],
                "file_path": {
                    "type": "string",
                    "description": "File path to list file content from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
