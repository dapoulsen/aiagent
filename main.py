import os
from google import genai
from dotenv import load_dotenv
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=sys.argv[1]
)

def main():

    if len(sys.argv) < 2:
        print("You need to provide a prompt!")
        sys.exit(1)
    
    print(response.text)
    print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
    print("Response tokens: ", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
