import os
from google.genai import types
from dotenv import load_dotenv
from google import genai

def write_file(working_directory, file_path, content):
  try:
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([working_directory, full_path]) != working_directory:
      return f'Error: Cannot write to "{full_path}" as it is outside the permitted working directory'
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
      f.write(content)
      return f'Successfully wrote to "{full_path}" ({len(content)} characters written)'
  except Exception as e:
          return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates or overwrites the specified file within the working directory with the provided content, ensuring the path is valid and parent directories exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path of the file to create or overwrite within the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
    ),
)