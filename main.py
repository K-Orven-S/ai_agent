import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function  


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in environment.")
        sys.exit(1)

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

    
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    max_iterations = 20

    try:
        for _ in range(max_iterations):
            
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )

            
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

            
            function_call_parts: list[types.Part] = []

            if response.function_calls:
                for function_call_part in response.function_calls:
                    
                    function_call_result = call_function(
                        function_call_part, verbose=verbose
                    )

                    
                    if (
                        not function_call_result.parts
                        or not function_call_result.parts[0].function_response
                        or function_call_result.parts[
                            0
                        ].function_response.response is None
                    ):
                        raise RuntimeError(
                            "Fatal: tool did not return function_response.response"
                        )

                    tool_part = function_call_result.parts[0]
                    function_call_parts.append(tool_part)

                    
                    if verbose:
                        print(f"-> {tool_part.function_response.response}")

            
            if function_call_parts:
                tool_message = types.Content(
                    role="user",  
                    parts=function_call_parts,
                )
                messages.append(tool_message)

            
            has_function_calls = bool(response.function_calls)
            has_text = bool(response.text and response.text.strip())

            if not has_function_calls and has_text:
                
                print("Final response:")
                print(response.text)
                break
        else:
           
            print("Reached maximum iterations without a final response.")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
