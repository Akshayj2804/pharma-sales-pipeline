import os
import pandas as pd
import logging

from config.config import RAW_FOLDER, CHECKPOINT_FILE
from src.utils import list_files_sorted

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_last_processed():
    """Retrieve the last processed file from checkpoint."""
    try:
        if not os.path.exists(CHECKPOINT_FILE):
            logger.info("No checkpoint file found. Starting fresh.")
            return None
        
        with open(CHECKPOINT_FILE, "r") as f:
            last_file = f.read().strip()
            logger.info(f"Last processed file: {last_file}")
            return last_file
    except Exception as e:
        logger.error(f"Error reading checkpoint: {e}")
        return None


def update_checkpoint(file_name):
    """Update checkpoint with the latest processed file."""
    try:
        # Ensure checkpoint directory exists
        os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)
        
        with open(CHECKPOINT_FILE, "w") as f:
            f.write(file_name)
        logger.info(f"Checkpoint updated: {file_name}")
    except Exception as e:
        logger.error(f"Failed to update checkpoint: {e}")
        raise


def get_next_file(files, last_file):
    """Get the next file to process based on checkpoint."""
    if not files:
        logger.warning("No files found in directory.")
        return None
    
    if last_file is None:
        next_file = files[0]
        logger.info(f"No previous checkpoint. Starting with: {next_file}")
        return next_file
    
    for f in files:
        if f > last_file:
            logger.info(f"Next file to process: {f}")
            return f
    
    logger.info("All files have been processed.")
    return None


def extract_next_batch():
    """
    Extract the next batch of data from parquet files.
    
    Returns:
        tuple: (DataFrame, filename) if successful, None if no new files
    """
    try:
        # Get sorted list of files
        files = list_files_sorted(RAW_FOLDER)
        
        if not files:
            logger.warning(f"No parquet files found in {RAW_FOLDER}")
            return None
        
        logger.info(f"Found {len(files)} total files in {RAW_FOLDER}")
        
        # Get last processed file
        last_file = get_last_processed()
        
        # Determine next file to process
        next_file = get_next_file(files, last_file)
        
        if next_file is None:
            logger.info("No new files to process.")
            return None
        
        # Read parquet file
        file_path = os.path.join(RAW_FOLDER, next_file)
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        
        logger.info(f"Reading file: {file_path}")
        df = pd.read_parquet(file_path)
        
        logger.info(f"Successfully loaded {len(df)} records from {next_file}")
        
        # Basic validation
        if df.empty:
            logger.warning(f"File {next_file} is empty!")
            return None
        
        return df, next_file
        
    except Exception as e:
        logger.error(f"Error in extract_next_batch: {e}", exc_info=True)
        raise