import os
import subprocess

def run_python_file(working_directory, file_path : str, args=[]):
    abs_working_directory = os.path.abspath(working_directory) 
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        final_args = ['uv', 'run', file_path]
        final_args.extend(args)

        # Set up environment with UTF-8 encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        output = subprocess.run(final_args, 
                                capture_output=True, 
                                text=True, 
                                timeout=30, 
                                cwd=abs_working_directory,
                                env=env,  
                                encoding='utf-8',  
                                errors='replace')
        final_string =  f'''
STDOUT: {output.stdout}
STDERR: {output.stderr}

        '''
        if not output.stdout and not output.stderr:
            final_string = "No output produced.\n"
        if output.returncode != 0:
            final_string += f'Process exited with code {output.returncode}'
        return final_string
    except Exception as e:
        return f"Error: executing Python file: {e}"