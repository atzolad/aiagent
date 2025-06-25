import os

def write_file(working_directory, file_path, content):

    relative_file_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(relative_file_path)
    abs_working_directory = os.path.abspath(working_directory)

    try:

        if os.path.commonpath([abs_file_path, abs_working_directory]) != abs_working_directory:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        file_directory = os.path.dirname(abs_file_path)
        os.makedirs(file_directory, exist_ok=True)
        
        with open(abs_file_path, 'w') as file:
            file.write(content)
            

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}"