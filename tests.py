from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
def main(): 
    working_directory = "calculator"
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file(working_directory, "../main.py"))

if __name__ == "__main__": 
    main() 

    