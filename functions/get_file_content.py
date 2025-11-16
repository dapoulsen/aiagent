import os 
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work_dir = os.path.abspath(working_directory)
    if os.path.commonpath([target_path, abs_work_dir]) != abs_work_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        return_string = ""
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            return_string = file_content_string
            if os.path.getsize(target_path) > MAX_CHARS:
                return_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return return_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
    
