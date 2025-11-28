import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    if len(sys.argv) <= 1:
        print("Please provide a prompt")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = len(sys.argv) > 2 and sys.argv[-1] == "--verbose"

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    
    function_call_parts = []

    if response.function_calls:
        for function_call_part in response.function_calls:
    
            function_call_result = call_function(function_call_part, verbose=verbose)

        
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
                or function_call_result.parts[0].function_response.response is None
            ):
                raise RuntimeError(
                    "Fatal: tool did not return function_response.response"
                )

            tool_part = function_call_result.parts[0]
            function_call_parts.append(tool_part)

            
            if verbose:
                print(f"-> {tool_part.function_response.response}")
    else:
        
        if verbose:
            print(f"User prompt: {response.text}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            print(response.text)


if __name__ == "__main__":
    main()
