import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try: 
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        if os.path.commonpath([target_file, working_directory_abs]) != working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_file[len(target_file)-3:] != '.py':
            return f'Error: "{file_path}" is not a Python file'
        command = ['python', target_file]
        if args != None:
            command.extend(args)
        result = subprocess.run(command, cwd = working_directory_abs, capture_output = True, text = True, timeout = 30)
        output = ""
        if result.returncode != 0:
            output += f'Process exited with code {result.returncode}\n'
        if result.stdout + result.stderr == '':
            output += 'No output produced'
        if result.stdout != '':
            output += f'STDOUT: {result.stdout}'
        if result.stderr != '':
            output += f'STDERR: {result.stderr}'
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Attemps to run a python file at a specified file path with args(default=None) and returns its output or exception.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the python file relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="(optional) Arguments to be passed into the python function"
            )
        },
    ),
)