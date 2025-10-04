import subprocess
import os

def run_python_file(working_directory, file_path, args=[]):
  try:
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([working_directory, full_path]) != working_directory:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
      return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
      return f'Error: "{file_path}" is not a Python file.'
    if not args:
      result = subprocess.run(["uv", "run", full_path], cwd=working_directory, timeout=30, capture_output=True, text=True)
    else:
      result = subprocess.run(["uv", "run", full_path, *args], cwd=working_directory, timeout=30, capture_output=True, text=True)
    output = f'STDOUT:{result.stdout}\n STDERR:{result.stderr}'
    if not result.stdout and not result.stderr:
        return "No output produced."
    elif result.returncode == 0:
        return output
    else:
        return f'{output}\n Process exited with code {result.returncode}'
  except Exception as e:
    return f"Error: executing Python file: {e}"
      
      
    
