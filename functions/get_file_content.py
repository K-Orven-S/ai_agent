import os
from config import MAX_CHARS



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

        

        
