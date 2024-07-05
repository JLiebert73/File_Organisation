import os
from .utils import shift
from shutil import move


def revert_file(source_path, destination_path):
    shift(source_path, destination_path)
    print(f"Reverted file: {destination_path} to {source_path}")


def move_files(source_dir):
    categories = {'Images', 'Videos', 'Code', 'Folders', 'Text', 'Others'}

    folder_count = 0
    image_count = 0
    text_count = 0
    video_count = 0
    code_count = 0
    other_count = 0

    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        if os.path.isdir(source_path) and filename in categories:
            if filename == 'Folders':
                folder_count = len(os.listdir(source_path))
            elif filename == 'Images':
                image_count = len(os.listdir(source_path))
            elif filename == 'Text':
                text_count = len(os.listdir(source_path))
            elif filename == 'Videos':
                video_count = len(os.listdir(source_path))
            elif filename == 'Code':
                code_count = len(os.listdir(source_path))

            for file in os.listdir(source_path):
                file_path = os.path.join(source_path, file)
                revert_file(file_path, source_dir)
                other_count += 1

    # Print the summary of files reverted
    print("\n\nAll files reverted successfully!")
    print("Folders reverted:", folder_count)
    print("Images reverted:", image_count)
    print("Text reverted:", text_count)
    print("Videos reverted:", video_count)
    print("Code reverted:", code_count)
    print("Others reverted:", other_count)


def main():
    source_dir = os.getcwd()
    move_files(source_dir)


if __name__ == "__main__":
    main()
