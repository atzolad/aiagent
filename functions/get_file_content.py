import os
from google.genai import types

def get_file_content(working_directory, file_path):
    relative_file_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(relative_file_path)
    abs_working_directory = os.path.abspath(working_directory)
    max_chars = 10000

    try:

        if os.path.commonpath([abs_file_path, abs_working_directory]) != abs_working_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_file_path, "r", encoding="utf-8") as file:
            file_content_string = file.read(max_chars)

        if os.path.getsize(abs_file_path) >= max_chars:
            return file_content_string + (f'[...File "{file_path}" truncated at {max_chars} characters.]')
        else:
            return file_content_string


    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Opens the file in the specified filepath and returns a max of 10000 characters. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to the file you want to open, relative to the working directory.",
            ),
        },
    ),
)
