import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    working_dir_full_path = os.path.abspath(working_directory)
    target_dir_full_path = working_dir_full_path
    if directory:
        target_dir_full_path = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir_full_path.startswith(working_dir_full_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir_full_path):
        return f'Error: "{directory}" is not a directory'
    try:
        dir_list = os.listdir(target_dir_full_path)
        result = []
        for dir_or_file in dir_list:
            dir_or_file_path = os.path.abspath(os.path.join(target_dir_full_path, dir_or_file))
            result.append(f"- {dir_or_file}: file_size={os.path.getsize(dir_or_file_path)}, is_dir={os.path.isdir(dir_or_file_path)}")
        return "\n".join(result)
    except Exception as e:
        return f"Error listing files: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
    