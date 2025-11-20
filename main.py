import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
from config import SYSTEM_PROMPT

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser()
parser.add_argument("prompt")
parser.add_argument('--verbose', help="show more information", action="store_true")

def main():

    args = parser.parse_args()

    user_prompt = args.prompt
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    )
    
    if args.verbose:

        print("User prompt: ", user_prompt)

        print(response.text)

        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)
    else:
        print(response.text)


if __name__ == "__main__":
   
    main()
