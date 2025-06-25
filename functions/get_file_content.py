import os

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