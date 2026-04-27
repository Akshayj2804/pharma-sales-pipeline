import os

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def list_files_sorted(folder, extension=".parquet"):
    files = [f for f in os.listdir(folder) if f.endswith(extension)]
    return sorted(files)