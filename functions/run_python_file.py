import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):

    relative_file_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(relative_file_path)
    abs_working_directory = os.path.abspath(working_directory)

    try:

        if os.path.commonpath([abs_file_path, abs_working_directory]) != abs_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'      

    except Exception as e:
        return f"Error: {e}"
    
    try:

        result = subprocess.run(["python3", abs_file_path], cwd=abs_working_directory, capture_output=True, check=True, text=True, timeout=30)

        exit_code = result.returncode
        output = (f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}")

        if not result.stdout and not result.stderr:
            return "No output produced."

    
        if exit_code != 0:
            output += (f"\nProcess exited with code {exit_code}")

        return output

    except subprocess.CalledProcessError as e:
        output = (f"STDOUT: {e.stdout}\nSTDERR: {e.stderr}")
        output += (f"Process exited with code {e.returncode}")
        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file at the given filepath. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to the python file you want to run, relative to the working directory.",
            ),
        },
    ),
)