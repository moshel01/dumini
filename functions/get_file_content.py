MAX_CHARS = 10000
import os

def get_file_content(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if os.path.commonpath([target_file, working_directory_abs]) != working_directory_abs:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(target_file) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(target_file) as file:
        content = file.read(MAX_CHARS)
        if file.read(1):
            content += f'[...File "{target_file}" truncated at {MAX_CHARS} characters]'
    return content