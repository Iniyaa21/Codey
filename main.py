import os 
import sys
from dotenv import load_dotenv 
from google import genai 
from google.genai import types

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

    #Save messages
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    #Set up client and get response
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )

    if is_verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count) 
        print("Response tokens: ", response.usage_metadata.candidates_token_count) 
        print() 
    
    #Print output
    print(response.text)

if __name__ == "__main__":
    main()