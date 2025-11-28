import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
        
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_directory, full_path]) != working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    if os.path.isdir(full_path):
        return f'Error: "{file_path}" is a directory, not a Python file.'

    
    cmd = ["python", file_path, *args]
    
    try:
        completed = subprocess.run(
            cmd,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        stdout = (completed.stdout or "").strip()
        stderr = (completed.stderr or "").strip()

        parts = []

        if stdout:
            parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            parts.append(f"STDERR:\n{stderr}")

        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")
        
        if not parts:
            return "No output produced."

        return "\n".join(parts)

    except subprocess.TimeoutExpired:
        return "Error: Process time out after 30 seconds."
    except Exception as e:
        return f"Error: {e}"