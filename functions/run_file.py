import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    working_dir_full_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_path.startswith(working_dir_full_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python", full_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=working_dir_full_path,
        )
        output = ""
        if result.stdout:
            output += f"STDOUT: {result.stdout}\n"
        if result.stderr:
            output += f"STDERR: {result.stderr}\n"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n" 
        return output if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"