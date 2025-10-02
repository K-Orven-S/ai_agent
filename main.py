import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)



def main():
    
    if len(sys.argv) == 1:
        print("Error: Please provide a prompt")
        sys.exit(1)
    elif "--verbose" in sys.argv:  
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}") 
        print(response.text)
    else:
        print(response.text)
        


if __name__ == "__main__":
    main()
