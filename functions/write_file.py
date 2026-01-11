import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if os.path.commonpath([target_file, working_directory_abs]) != working_directory_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    os.makedirs(file_path, exist_ok=True)
    with open(target_file, "w") as file:
        file.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Attemps to write to a file of a specified file path with specified content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the python file relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that is to be written to the file."
            )
        },
    ),
)