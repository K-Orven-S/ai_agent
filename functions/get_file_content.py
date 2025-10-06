import os
from .config import MAX_CHARS
from google.genai import types
from dotenv import load_dotenv
from google import genai

def get_file_content(working_directory, file_path):
  try:
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([working_directory, full_path]) != working_directory:
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
      return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(full_path, "r", encoding="utf-8") as f:
      file_content_string = f.read(MAX_CHARS + 1)
      if len(file_content_string) > MAX_CHARS:
        file_content_string = file_content_string[:MAX_CHARS]
        file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
      return file_content_string
      
  except Exception as e:
    return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of the specified file within the working directory, truncating if it exceeds MAX_CHARS.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file within the working directory to read from.",
            ),
        },
    ),
)
