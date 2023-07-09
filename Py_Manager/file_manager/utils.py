import os


def create_directory(directory_path):
    os.makedirs(directory_path, exist_ok=True)


def shift(source_path, destination_path):
    try:
        os.rename(source_path, destination_path)
        print(f"Moved file: {source_path} to {destination_path}")
    except Exception as e:
        print(f"Error moving file: {str(e)}")


def main():
    # Get the current working directory
    path = os.getcwd()
    source_dir = path
    destination_dir = path

    # Call the shift() function to move files
    shift(source_dir, destination_dir)


if __name__ == "__main__":
    main()
