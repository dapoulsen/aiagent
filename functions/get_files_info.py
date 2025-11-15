import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_full_path = os.path.abspath(full_path)
    abs_work_dir = os.path.abspath(working_directory)

    if os.path.commonpath([abs_full_path, abs_work_dir]) != abs_work_dir:                                           
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_full_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        entries = os.listdir(abs_full_path)
        lines = []
        for entry in entries:
            p = os.path.join(abs_full_path, entry)
            size = os.path.getsize(p)
            is_dir = os.path.isdir(p)
            lines.append(f'- {entry}: file_size={size} bytes, is_dir={is_dir}')
        return "\n".join(lines)
    except Exception as e:
        return f'Error: {e}'

