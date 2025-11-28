import os
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def print_dir_result(working_directory: str, file_path: str, args=[]):
    print(f'run_python_file"{working_directory}", "{file_path}"):')

    result = run_python_file(working_directory, file_path, args)

    print(result)

def main():
    
    print_dir_result("calculator", "main.py")
    print_dir_result("calculator", "main.py", ["3 + 5"])
    print_dir_result("calculator", "tests.py")
    print_dir_result("calculator", "../main.py")
    print_dir_result("calculator", "nonexistent.py")
    print_dir_result("calculator", "lorem.txt")

if __name__ == "__main__":
    main()
