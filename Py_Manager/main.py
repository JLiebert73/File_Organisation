import os
from tabulate import tabulate
from file_manager.sort import move_files
from file_manager.revert import move_files as revert_files
from file_manager.metadata import compile_metadata
from file_manager.compress import compress_text, decompress_text

def main():
    current_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    text_dir = os.path.join(current_dir, 'Text')

    print("Welcome to Py_Manager!")
    print("Please select an option:")
    print("1. Sort files")
    print("2. Revert file movements")
    print("3. Extract file metadata")
    print("4. Compress text")
    print("5. Decompress text")

    option = input("Enter the option number: ")

    if option == "1":
        source_dir = current_dir
        destination_dir = current_dir
        move_files(source_dir, destination_dir)
        print("Files sorted and moved successfully!")
    elif option == "2":
        directory = current_dir
        revert_files(directory)
        print("File movements reverted successfully!")
    elif option == "3":
        extension = input("Enter the file extension to retrieve metadata for (e.g., .jpg, .pdf, .docx): ")
        metadata = compile_metadata(text_dir, extension)

        if metadata:
            headers = ['File', 'Type']
            if extension == '.pdf':
                headers.extend(['Num Pages', 'Title', 'Author', 'Subject'])
            elif extension in ['.docx', '.doc']:
                headers.extend(['Title', 'Author', 'Created'])
            elif extension == '.xlsx':
                headers.extend(['Title', 'Author', 'Created'])
            elif extension == '.pptx':
                headers.extend(['Title', 'Author', 'Created'])
            elif extension == '.png':
                headers.extend(['Format', 'Size', 'Mode'])
            elif extension == '.txt':
                headers.append('Content')

            data = []
            for item in metadata:
                file_name = os.path.basename(item[1])
                file_data = [file_name, item[0]]
                file_data.extend(item[2:])
                data.append(file_data)

            print(tabulate(data, headers=headers, tablefmt='grid'))
        else:
            print('No files with the specified extension found in the directory.')
    elif option == "4":
        file_path = input("Enter the file path to compress (with .txt extension): ")
        compress_text(file_path)
    elif option == "5":
        file_path = input("Enter the file path to decompress (with .bin extension): ")
        decompress_text(file_path)
    else:
        print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
