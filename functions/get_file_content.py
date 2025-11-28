import os
from config import MAX_CHARS
from google.genai import types



def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_directory, full_path]) != working_directory:
        return f'Error: Cannot read "{full_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{full_path}"'
    
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string = f.read(MAX_CHARS)
                return file_content_string + f"[...File {file_path} truncated at 10000 characters]"
            else:
                return file_content_string

    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Reads the contents of a file within the working directory, returning up to "
        "MAX_CHARS characters and indicating if the content was truncated."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the file to read, relative to the working directory. "
                    "Must refer to a regular file inside the working directory."
                ),
            ),
        },
        required=["file_path"],
    ),
)
        

        
