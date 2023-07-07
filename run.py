import os
import shutil

def shift(source_path, destination_path):
    try:
        # Move the file from source to destination
        shutil.move(source_path, destination_path)
        print(f"Moved file: {source_path} to {destination_path}")
    except Exception as e:
        print(f"Error moving file: {str(e)}")

def main():
    # Get the current working directory
    path = os.getcwd()
    source_dir = path
    destination_dir = path

    # Initialize counters for different file categories
    Images = 0
    Text = 0
    Code = 0
    Videos = 0
    Folders = 0
    Others = 0

    # Create destination directories if they don't exist
    os.makedirs(destination_dir, exist_ok=True)
    image_dir = os.path.join(destination_dir, "Images")
    text_dir = os.path.join(destination_dir, "Text")
    video_dir = os.path.join(destination_dir, "Videos")
    code_dir = os.path.join(destination_dir, "Code")
    others_dir = os.path.join(destination_dir, "Others")
    folders_dir = os.path.join(destination_dir, "Folders")
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(code_dir, exist_ok=True)
    os.makedirs(others_dir, exist_ok=True)
    os.makedirs(folders_dir, exist_ok=True)

    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        if os.path.isfile(source_path):
            # Get the file extension
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                Images += 1
                destination_path = os.path.join(image_dir, filename)
                shift(source_path, destination_path)
            elif file_extension in ['.txt', '.doc', '.pdf', '.ppt', '.xls']:
                Text += 1
                destination_path = os.path.join(text_dir, filename)
                shift(source_path, destination_path)
            elif file_extension in ['.mp4', '.mov', '.avi', '.mkv', '.srt']:
                Videos += 1
                destination_path = os.path.join(video_dir, filename)
                shift(source_path, destination_path)
            elif file_extension in ['.cc', '.exe', '.py', '.c']:
                # Exclude specific files from being moved
                if filename == "run.py" or filename == "revert.py":
                    continue
                Code += 1
                destination_path = os.path.join(code_dir, filename)
                shift(source_path, destination_path)
            else:
                Others += 1
                destination_path = os.path.join(others_dir, filename)
                shift(source_path, destination_path)
        elif os.path.isdir(source_path):
            # Exclude category directories from being moved
            if filename not in ['Images', 'Text', 'Videos', 'Code', 'Folders', 'Others']:
                Folders += 1
                destination_path = os.path.join(folders_dir, filename)
                shift(source_path, destination_path)

    # Print the summary of files moved
    print("\n\nAll files sorted successfully!")
    print("\n\nFolders moved : ", Folders)
    print("Images moved  : ", Images)
    print("Text moved    : ", Text)
    print("Videos moved  : ", Videos)
    print("Code moved    : ", Code)
    print("Others moved  : ", Others)

if __name__ == "__main__":
    main()
