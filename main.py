import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python_file



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
        schema_write_file,
        schema_run_python_file,
    ]
)


dispatch = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
       

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    if function_name not in dispatch:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    func = dispatch[function_call_part.name]
    function_result = func("./calculator", **function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

    

def main():
    
    if len(sys.argv) == 1:
        print("Error: Please provide a prompt")
        sys.exit(1)

    message_history = []
    repeat = 0
    user_prompt = sys.argv[1]
    messages = [
                types.Content(role="user", parts=[types.Part(text=user_prompt)]),
            ]
    message_history.extend(messages)

   

    while repeat < 20:
        had_text = False
        had_function_call = False
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=message_history,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            model_reply = response.candidates[0].content

            for part in model_reply.parts:

                if "--verbose" in sys.argv:
                    print(f"User prompt: {user_prompt}")
                    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

                    if part.text:
                        print(part.text)
                        had_text = True

                    if part.function_call:
                        had_function_call = True
                        function_call_part = part.function_call
                        try:
                            function_call_result = call_function(function_call_part, verbose=True)
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                            message_history.append(model_reply)
                            message_history.append(function_call_result)
                            repeat += 1
                        except Exception as e:
                            print(f"Error calling {function_call_part.name}: {e}")

                else:
                    if part.text:
                        print(part.text)
                        had_text = True

                    if part.function_call:
                        had_function_call = True
                        function_call_part = part.function_call
                        try:
                            function_call_result = call_function(function_call_part)
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                            message_history.append(model_reply)
                            message_history.append(function_call_result)
                            repeat += 1
                        except Exception as e:
                            print(f"Error: {e}")

            if had_text and not had_function_call:
                break

        except Exception as e:
            print(f"Error: {e}")
    

if __name__ == "__main__":
    main()
