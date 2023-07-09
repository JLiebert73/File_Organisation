import os
from .utils import create_directory, shift
from .metadata import extract_image_metadata, extract_pdf_metadata, extract_docx_metadata, extract_xlsx_metadata, extract_pptx_metadata


def move_files(source_dir, destination_dir):
    create_directory(destination_dir)

    categories = {
        '.jpg': 'Images',
        '.jpeg': 'Images',
        '.png': 'Images',
        '.gif': 'Images',
        '.txt': 'Text',
        '.doc': 'Text',
        '.pdf': 'Text',
        '.ppt': 'Text',
        '.xls': 'Text',
        '.mp4': 'Videos',
        '.mov': 'Videos',
        '.avi': 'Videos',
        '.mkv': 'Videos',
        '.srt': 'Videos',
        '.cc': 'Code',
        '.exe': 'Code',
        '.py': 'Code',
        '.c': 'Code'
    }

    folder_count = 0
    image_count = 0
    text_count = 0
    video_count = 0
    code_count = 0
    other_count = 0

    for filename in os.listdir(source_dir):
        if filename == "Py_Manager" and os.path.isdir(os.path.join(source_dir, filename)):
            continue
        source_path = os.path.join(source_dir, filename)
        if os.path.isfile(source_path):
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension in categories:
                destination_category = categories[file_extension]
                destination_category_dir = os.path.join(destination_dir, destination_category)
                create_directory(destination_category_dir)
                destination_path = os.path.join(destination_category_dir, filename)
                shift(source_path, destination_path)
                if destination_category == 'Folders':
                    folder_count += 1
                elif destination_category == 'Images':
                    image_count += 1
                elif destination_category == 'Text':
                    text_count += 1
                elif destination_category == 'Videos':
                    video_count += 1
                elif destination_category == 'Code':
                    code_count += 1
            else:
                other_dir = os.path.join(destination_dir, 'Others')
                create_directory(other_dir)
                destination_path = os.path.join(other_dir, filename)
                shift(source_path, destination_path)
                other_count += 1
        elif os.path.isdir(source_path):
            folders_dir = os.path.join(destination_dir, 'Folders')
            create_directory(folders_dir)
            destination_path = os.path.join(folders_dir, filename)
            shift(source_path, destination_path)
            folder_count += 1

    # Print the summary of files moved
    print("\n\nAll files sorted successfully!")
    print("Folders moved:", folder_count)
    print("Images moved:", image_count)
    print("Text moved:", text_count)
    print("Videos moved:", video_count)
    print("Code moved:", code_count)
    print("Others moved:", other_count)


def main():
    source_dir = os.getcwd()
    destination_dir = os.getcwd()

    move_files(source_dir, destination_dir)


if __name__ == "__main__":
    main()
