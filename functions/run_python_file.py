import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work_dir = os.path.abspath(working_directory)

    if os.path.commonpath([full_path, abs_work_dir]) != abs_work_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ["python", full_path] + args,   # command to execute
            cwd=abs_work_dir,               # working directory
            stdout=subprocess.PIPE,         # capture stdout
            stderr=subprocess.PIPE,         # capture stderr
            timeout=30,                     # timeout in seconds
            text=True                       # return strings instead of bytes
        )  
        print_result = f'STDOUT: {result.stdout} \nSTDERR: {result.stderr}'
        if result.returncode != 0:
            print_result += f"\nProcessed exited with code {result.returncode}"
        if len(result.args) == 0:
            print_result = "No output produced"
        return print_result

    except Exception as e:
        return f"Error: executing Python file: {e}"