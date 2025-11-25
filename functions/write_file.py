import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work_dir = os.path.abspath(working_directory)
    if os.path.commonpath([full_path, abs_work_dir]) != abs_work_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        if os.path.exists(file_path):
            os.makedirs(file_path)
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the given content to the given file, constrained to the current working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Write to the given file. If not provided, return an error",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The given content that is to be written to the file. If not provided, do nothing."
            )
        },
    ),
)