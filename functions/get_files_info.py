import os

def get_files_info(working_directory, directory="."):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    
    if os.path.commonpath([working_directory, full_path]) != working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        results = []

        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            
            results.append(f"{item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"Error: {e}"