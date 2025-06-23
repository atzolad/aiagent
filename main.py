import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) <= 1:
    print('Invalid Prompt')
    sys.exit(1)

else:
    user_prompt = sys.argv[1] #Take a command line input for the prompt.


#Keep a list to record the messages that have already been sent to the AI agent
messages = [
    types.Content(role="user", parts =[types.Part(text=user_prompt)]),
]

#Send the prompt to the AI agent
response = client.models.generate_content(
    model = "gemini-2.0-flash-001",
    contents = messages,
)


print(response.text)

#Keep track of the API usage data
if response.usage_metadata:

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

else:
    print("Usage Metadata not available in the response")

if sys.argv[-1] == "--verbose":
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

