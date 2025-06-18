import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    working_dir_full_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_path.startswith(working_dir_full_path):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path, "r") as f:
            content = f.read(MAX_CHARS + 1)
            if len(content) == MAX_CHARS + 1:
                content = content[:-1]
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: attempting to read file: {file_path} resulted in error: {e}"
    