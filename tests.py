from functions.get_files_info import get_files_info 

def main(): 
    list_of_directories = [".", "pkg", "/bin", "../"]
    for directory in list_of_directories: 
        print(f"Result for '{directory}' directory:")
        result = get_files_info("calculator", directory)
        if not result.startswith("Error"): 
            lines = result.split("\n") 
            for line in lines:
                print("- " + line)
        else: 
            print(result)
        print()
if __name__ == "__main__": 
    main() 