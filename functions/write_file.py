import os

def write_file(working_directory, file_path, content):

    relative_file_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(relative_file_path)
    abs_working_directory = os.path.abspath(working_directory)

    try:

        if not abs_file_path.startswith(abs_working_directory):
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

        if not os.path.exists(abs_file_path):
            file_directory = os.path.dirname(abs_file_path)
            os.makedirs(file_directory, mode=0o777, exist_ok=True)
        
        with open(abs_file_path, 'w', ) as file:
            file.write(content)
            

        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')


    except Exception as e:
        return(f"Error: {e}")