import os
import config
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of the specified file as a string, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory",
            ),
        },
    ),
)

MAX_CHARS = config.MAX_CHARS 

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path): 
        return f'Error: File not found or is not a regular file: "{file_path}"'
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(abs_file_path, "r", encoding=encoding) as f:
                file_content_string = f.read(MAX_CHARS)
                if len(file_content_string) >= MAX_CHARS:
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content_string
        except UnicodeDecodeError:
            continue  # Try next encoding
        except Exception as e:
            return f'Error: {e}'
    
    # If all encodings fail, try with error replacement
    try:
        with open(abs_file_path, "r", encoding='utf-8', errors='replace') as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string + "\n[Note: Some characters may have been replaced due to encoding issues]"
    except Exception as e:
        return f'Error: Unable to read file with any encoding: {e}'

