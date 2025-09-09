from functions.get_file_content import get_file_content

def main(): 
    list_of_files = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]
    for filepath in list_of_files: 
        print(get_file_content("calculator", filepath))
        print("*"*100)
        
if __name__ == "__main__": 
    main() 

    