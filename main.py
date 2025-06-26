import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types
from call_function import call_function, available_functions
from prompts import system_prompt


# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


if len(sys.argv) <= 1:
    print('Invalid Prompt')
    sys.exit(1)

else:
    #creates a list of arguments passed to the program through the console input.
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    user_prompt = ''.join(args) #Take a command line input for the prompt. Joins multiple arguments
    if sys.argv[-1] == "--verbose": #Set verbose status based on user input
        verbose = True
    else:
        verbose = False


#Keep a list to record the messages that have already been sent to the AI agent
messages = [
    types.Content(role="user", parts =[types.Part(text=user_prompt)]),
]

if verbose:
    print(f'User prompt: {user_prompt}')

for i in range (20):
    #Send the prompt to the AI agent
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    #Keep track of the API usage data
    if response.usage_metadata:

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

    else:
        print("Usage Metadata not available in the response")

    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


    for candidate in response.candidates:
        messages.append(candidate.content)

    if response.function_calls:
        tool_response_parts = []
        for r in response.function_calls:
            result = call_function(r)
            try:
                function_call_result = result.parts[0]
                tool_response_parts.append(function_call_result)
                if verbose == True:
                    print(f"-> {result.parts[0].function_response.response}")

            except Exception as e:
                raise Exception(f"Error: {e}")
            
        final_function_calls = types.Content(role='tool', parts = tool_response_parts)
        messages.append(final_function_calls)
        continue

    else:
        print(response.text)
        break


#source venv/bin/activate'''