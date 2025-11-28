import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_directory, full_path]) != working_directory:
        return f'Error: Cannot write to "{full_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(full_path):
        return "Error: Cannot write to a directory"
    
    dir_path = os.path.dirname(full_path)
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
        except Exception as e:
            return f"Error creating directory: {e}"

    

    try:
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing file: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes text content to a file inside the working directory. "
        "Creates parent directories if needed, enforces security boundaries, "
        "and overwrites the file if it already exists."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the file to write, relative to the working directory. "
                    "Parent directories are created automatically if missing."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file."
            ),
        },
        required=["file_path", "content"],
    ),
)
