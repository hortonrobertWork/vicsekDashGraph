import os

def is_valid_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_line(line):
    values = line.strip().split()
    if len(values) != 4:
        return False
    for val in values:
        if not is_valid_float(val):
            return False
    return True

def validate_file(file_path):
    try:
        with open(file_path, 'r') as file:
            line_number = 0
            for line in file:
                line_number += 1
                if not validate_line(line):
                    print(f"Error in file {file_path}, line {line_number}: {line.strip()} is not a valid line.")
    except Exception as e:
        print(f"An error occurred while processing file {file_path}: {e}")

def main(directory_path):
    try:
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory_path, filename)
                validate_file(file_path)
    except FileNotFoundError:
        print(f"Directory '{directory_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    directory_path = input("Enter the path to the directory containing text files: ")
    main(directory_path)
