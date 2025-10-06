import os
from google.genai import types
from dotenv import load_dotenv
from google import genai

def get_files_info(working_directory, directory="."):
  try:
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    if os.path.commonpath([working_directory, full_path]) != working_directory:
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
      return f'Error: "{directory}" is not a directory'
    entries = os.listdir(full_path)
    if entries:
      result = []
      for file in entries:
        if os.path.isdir(os.path.join(full_path, file)):
          size = "-"
        else:
          size = os.path.getsize(os.path.join(full_path, file))
        result.append(f"- {file}: file_size={size}, is_dir={os.path.isdir(os.path.join(full_path, file))}")
      return '\n'.join(result)
    else:
      return f'"{directory}" is empty'
  except Exception as e:
      return f"Error: {str(e)}"

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