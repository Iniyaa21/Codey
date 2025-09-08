import os

def get_files_info(working_directory, directory = "."):
    abs_working_directory = os.path.abspath(working_directory) 
    abs_directory = os.path.abspath(os.path.join(working_directory, directory)) 
    if not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
    
    final_response = [] 
    contents = os.listdir(abs_directory) 
    for content in contents: 
        content_path = os.path.join(abs_directory, content) 
        size = os.path.getsize(content_path) 
        is_dir = os.path.isdir(content_path)
        final_response.append(f"{content}: file_size={size} bytes, is_dir={is_dir}")
    return "\n".join(final_response) 