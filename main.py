import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types
from call_function import call_function

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
touch 
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

#Give the LLM the ability to call functions

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content into the file at given filepath. If file doesn't exist, it is created. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to the file you want to open, relative to the working directory. ",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description="The content you want to write to the file."
            )
        },
    ),
)

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



available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

if len(sys.argv) <= 1:
    print('Invalid Prompt')
    sys.exit(1)

else:
    user_prompt = sys.argv[1] #Take a command line input for the prompt.
    if sys.argv[-1] == "--verbose": #Set verbose status based on user input
        verbose = True
    else:
        verbose = False


#Keep a list to record the messages that have already been sent to the AI agent
messages = [
    types.Content(role="user", parts =[types.Part(text=user_prompt)]),
]

#Send the prompt to the AI agent
response = client.models.generate_content(
    model = "gemini-2.0-flash-001",
    contents = messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
)



if response.function_calls:
    for r in response.function_calls:
        result = call_function(r)

        try:
            final_result = result.parts[0].function_response.response
            if verbose == True:
                print(f"-> {result.parts[0].function_response.response}")

        except Exception as e:
            raise Exception(f"Error: {e}")


        #print(f"Calling function: {r.name}({r.args})")
 
else:
    print(response.text)

#Keep track of the API usage data
if response.usage_metadata:

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

else:
    print("Usage Metadata not available in the response")

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

#source venv/bin/activate