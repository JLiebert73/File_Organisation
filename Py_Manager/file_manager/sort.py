import os
import concurrent.futures
from .utils import create_directory, shift
from .metadata import extract_image_metadata, extract_pdf_metadata, extract_docx_metadata, extract_xlsx_metadata, extract_pptx_metadata


def move_file(source_path, destination_dir, categories):
    filename = os.path.basename(source_path)
    file_extension = os.path.splitext(filename)[1].lower()
    if file_extension in categories:
        destination_category = categories[file_extension]
        destination_category_dir = os.path.join(destination_dir, destination_category)
        create_directory(destination_category_dir)
        destination_path = os.path.join(destination_category_dir, filename)
        shift(source_path, destination_path)
        return destination_category
    else:
        other_dir = os.path.join(destination_dir, 'Others')
        create_directory(other_dir)
        destination_path = os.path.join(other_dir, filename)
        shift(source_path, destination_path)
        return 'Others'


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

    counts = {
        'Folders': 0,
        'Images': 0,
        'Text': 0,
        'Videos': 0,
        'Code': 0,
        'Others': 0
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(source_dir):
            if filename == "Py_Manager" and os.path.isdir(os.path.join(source_dir, filename)):
                continue
            source_path = os.path.join(source_dir, filename)
            if os.path.isfile(source_path):
                futures.append(executor.submit(move_file, source_path, destination_dir, categories))
            elif os.path.isdir(source_path):
                folders_dir = os.path.join(destination_dir, 'Folders')
                create_directory(folders_dir)
                destination_path = os.path.join(folders_dir, filename)
                shift(source_path, destination_path)
                counts['Folders'] += 1

        for future in concurrent.futures.as_completed(futures):
            category = future.result()
            counts[category] += 1

    # Print the summary of files moved
    print("\n\nAll files sorted successfully!")
    print("Folders moved:", counts['Folders'])
    print("Images moved:", counts['Images'])
    print("Text moved:", counts['Text'])
    print("Videos moved:", counts['Videos'])
    print("Code moved:", counts['Code'])
    print("Others moved:", counts['Others'])


def main():
    source_dir = os.getcwd()
    destination_dir = os.getcwd()

    move_files(source_dir, destination_dir)


if __name__ == "__main__":
    main()
