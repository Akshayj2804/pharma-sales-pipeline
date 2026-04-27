import os
import pandas as pd

from config.config import RAW_FOLDER,CHECKPOINT_FILE
from src.utils import list_files_sorted

def get_last_processed():
    if not os.path.exists(CHECKPOINT_FILE):
        return None
    
    with open(CHECKPOINT_FILE,"r") as f:
        return f.read().strip()
    
def update_checkpoint(file_name):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(file_name)

def get_next_file(files, last_file):
    if last_file is None:
        return files[0] if files else None
    
    for f in files:
        if f> last_file:
            return f
    
    return None

def extract_next_batch():
    files = list_files_sorted(RAW_FOLDER)

    last_file = get_last_processed()

    next_file = get_next_file(files, last_file)

    if next_file is None:
        print("No new files to process.")
        return None
    
    file_path = os.path.join(RAW_FOLDER,next_file)

    df = pd.read_parquet(file_path)

    print(f"Processing file: {next_file}")
    
    return df, next_file
    
    