import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(target_dir) == False:
        return f'Error: "{directory}" is not a directory'
    response = f'Result for "{directory}" directory: \n'
    for thing in os.listdir(target_dir):
        response += f'- {thing}: file_size={os.path.getsize(target_dir + '/' +  thing)} bytes, is_dir={os.path.isdir(target_dir + '/' + thing)}\n'
    return response