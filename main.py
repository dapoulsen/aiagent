import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
from config import SYSTEM_PROMPT
from call_function import available_functions, call_function





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

    function_parts = []
   
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)
        part = function_call_result.parts[0]
        if not part.function_response or not part.function_response.response:
            raise Exception("Fatal exeption!!!")
        function_parts.append(part)

        if verbose:
           print(f"-> {function_call_result.parts[0].function_response.response}")
        
    # return function_parts
   
        




    
 

if __name__ == "__main__":
   
    main()
