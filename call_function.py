from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from run_python_file import run_python_file
from google.genai import types

def call_function(function_call_part, verbose=False):

    keyword_arguments = {}

    if verbose==True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        
    else:
        print(f" - Calling function: {function_call_part.name}")

    keyword_arguments['get_files_info'] = get_files_info
    keyword_arguments['get_file_content'] = get_file_content
    keyword_arguments['write_file'] = write_file
    keyword_arguments['run_python_file'] = run_python_file

    function_call_part.args.update({'working_directory': './calculator'})

    function_name = function_call_part.name
   
    if function_name not in  keyword_arguments:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    else:
        #print(f"DEBUG: Calling {function_name} with args: {function_call_part.args}")
        function_to_call = keyword_arguments[function_name]
        result = function_to_call(**function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result},
                )
            ],
        )