# functions/call_function.py
import os
from google.genai import types

from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .write_file import write_file
from .run_python_file import run_python_file

FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part: types.FunctionCall, verbose: bool = False) -> types.Content:
    function_name = function_call_part.name

    # Logging
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")

    func = FUNCTIONS.get(function_name)

    # Unknown function → return error as tool content
    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Build kwargs from LLM args + working_directory
    kwargs = dict(function_call_part.args)
    kwargs["working_directory"] = "./calculator"

    try:
        function_result = func(**kwargs)
    except Exception as e:
        function_result = f"Error during function execution: {e}"

    # Wrap the string result into {"result": ...}
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
