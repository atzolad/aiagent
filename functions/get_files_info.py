import os

def get_files_info(working_directory, directory=None):
    abs_directory = os.path.abspath(directory)
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_directory.startswith(abs_working_directory):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

    if not os.path.isdir(directory):
        return (f'Error: "{directory}" is not a directory')
    
    else:
        
        contents = os.listdir(directory)
        contents_list = []

        for file in contents:
            file_name = file
            file_path = os.path.join(directory, file)
            file_size = os.path.getsize(file_path)
            is_file_dir = os.path.isdir(file_path)
            #print(f"- {file_name}: file_size={file_size} bytes, is_dir={is_file_dir}")
            contents_list.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_file_dir}")

        print('\n'.join(contents_list))

get_files_info("/Users/alexzolad/workspace/github.com/atzolad/aiagent", "/Users/alexzolad/workspace/github.com/atzolad/aiagent")
