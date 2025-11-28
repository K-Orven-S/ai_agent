import os

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