import os 
import sys
from dotenv import load_dotenv 
from google import genai 
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

def main(): 
    #Check if prompt is given
    if len(sys.argv) < 2:
        print("No prompt provided!") 
        sys.exit(1)
    
    #Check for verbose flag
    is_verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose": 
        is_verbose = True
    
    #Load api key
    load_dotenv() 
    api_key = os.environ.get("GEMINI_API_KEY")
    
    #Get user prompt
    user_prompt = sys.argv[1]

    system_prompt = system_prompt = """
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
        schema_write_file
        ]
    )

    config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    )
    #Save messages
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    #Set up client and get response
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages, 
        config=config
    )
    
    if response is None or response.usage_metadata is None:
        print("Response is malformed") 
        return 

    #Print output

    if is_verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count) 
        print("Response tokens: ", response.usage_metadata.candidates_token_count) 
        print() 
    
    if response.function_calls:
        for function_call_part in response.function_calls:
            # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_result = call_function(function_call_part,is_verbose)
            response = function_call_result.parts[0].function_response.response
            if not response: 
                return 
            print(f"-> {response}")

    else:
        print(response.text) 

if __name__ == "__main__":
    main()