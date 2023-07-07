import os
import shutil

def shift(source_path, destination_path):
    try:
        # Move the file from source_path to destination_path
        shutil.move(source_path, destination_path)
        print(f"Moved file: {source_path} to {destination_path}")
    except Exception as e:
        print(f"Error moving file: {str(e)}")

def move_files(source_dir):
    # Initialize counters for different file categories
    Images = 0
    Text = 0
    Code = 0
    Videos = 0
    Folders = 0
    Others = 0

    # Define the directories that correspond to specific file categories
    dir = {"Images", "Videos", "Code", "Folders", "Text", "Others"}

    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        if os.path.isdir(source_path) and filename in dir:
            # Iterate through files in the category directory (e.g., "Images" or "Videos")
            for file in os.listdir(source_path):
                file_path = os.path.join(source_path, file)
                # Move the file into the source_dir using the shift() function
                shift(file_path, source_dir)

                # Update counters based on the category of the file
                if filename == "Images":
                    Images += 1
                elif filename == "Videos":
                    Videos += 1
                elif filename == "Code":
                    Code += 1
                elif filename == "Folders":
                    Folders += 1
                elif filename == "Text":
                    Text += 1
                else:
                    Others += 1
        else:
            # Do something else with non-directory files if needed
            pass

    # Print the summary of files moved
    print("\n\nAll files sorted successfully!")
    print("\n\nFolders moved : ", Folders)
    print("Images moved  : ", Images)
    print("Text moved    : ", Text)
    print("Videos moved  : ", Videos)
    print("Code moved    : ", Code)
    print("Others moved  : ", Others)

def main():
    # Get the current working directory
    path = os.getcwd()
    source_dir = path
    move_files(source_dir)

if __name__ == "__main__":
    main()
