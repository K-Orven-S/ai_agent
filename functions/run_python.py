import subprocess
import os
from google.genai import types
from dotenv import load_dotenv
from google import genai

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

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory using subprocess, passing optional arguments, enforcing a 30-second timeout, capturing stdout and stderr, and returning results or errors.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file within the working directory to execute.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file.",
            ),
        },
    ),
)
      
      
    
