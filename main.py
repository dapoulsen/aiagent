import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
from config import SYSTEM_PROMPT
from call_function import available_functions





def main():
    load_dotenv()


    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument('--verbose', help="show more information", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = args.prompt
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


    verbose = args.verbose

    if verbose:
        print(f'User prompt: {user_prompt}\n')
    
    generate_content(client, messages, verbose)
    

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
            )
    )

   
    if verbose:
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    for call in response.function_calls:
        print(f'Calling function: {call.name}({call.args})')
 

if __name__ == "__main__":
   
    main()
