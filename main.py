import os
import sys
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
    
    iterations = 0
    while True:
        iterations += 1
        if iterations > 15:
            print(f'Maximum iterations of 15 is reached')
            sys.exit(1)
        
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print('Final response:')
                print(final_response)
                break
        
        except Exception as e:
            print(f'Error in generate_content: {e}')

    

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
    
    if response.cadidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []

   
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call results")
        if verbose:
            print(f'-> {function_call_result.parts[0].function_response.response}')
        function_responses.append(function_call_result.parts[0])
    
    if not function_responses:
        raise Exception("No function responses generated, exiting.")
    
    messages.append(types.Content(role="user", parts=function_responses))
        
    # return function_parts
   
        




    
 

if __name__ == "__main__":
   
    main()
