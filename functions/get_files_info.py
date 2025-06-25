import os

def get_files_info(working_directory, directory=None):

    if directory is None:
        relative_directory = working_directory
    else:
        relative_directory = os.path.join(working_directory, directory)

    abs_directory = os.path.abspath(relative_directory)
    abs_working_directory = os.path.abspath(working_directory)


    try:

        if os.path.commonpath([abs_directory, abs_working_directory]) != abs_working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            #print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'
            #print(f'Error: "{directory}" is not a directory')
        
        else:
            
            contents = os.listdir(abs_directory)
            contents_list = []

            for file in contents:
                file_name = file
                file_path = os.path.join(abs_directory, file)
                file_size = os.path.getsize(file_path)
                is_file_dir = os.path.isdir(file_path)
                #print(f"- {file_name}: file_size={file_size} bytes, is_dir={is_file_dir}")
                contents_list.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_file_dir}")

            return '\n'.join(contents_list)
            #print(('\n'.join(contents_list)))

    except Exception as e:
        return f"Error: {e}"


