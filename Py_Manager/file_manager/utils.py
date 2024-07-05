import os
import shutil
from tf_idf import HNSW

def create_directory(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def shift(source_path, destination_path):
    try:
        if os.path.isfile(source_path):
            shutil.move(source_path, destination_path)
        elif os.path.isdir(source_path):
            shutil.move(source_path, destination_path)
        print(f"Moved: {source_path} to {destination_path}")
    except Exception as e:
        print(f"Error moving {source_path} to {destination_path}: {e}")

def main():
    hnsw = HNSW(m=16, ef_construction=200)
    path = os.getcwd()
    source_dir = path
    destination_dir = path
    shift(source_dir, destination_dir)

if __name__ == "__main__":
    main()
