import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_dir(path):
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(f"Created directory: {path}")
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        raise


def list_files_sorted(folder, extension=".parquet"):
    """
    List files in folder with specified extension, sorted alphabetically.
    
    Args:
        folder: Folder path
        extension: File extension to filter
        
    Returns:
        Sorted list of filenames
    """
    try:
        if not os.path.exists(folder):
            logger.warning(f"Folder does not exist: {folder}")
            return []
        
        files = [f for f in os.listdir(folder) if f.endswith(extension)]
        files_sorted = sorted(files)
        
        logger.info(f"Found {len(files_sorted)} {extension} files in {folder}")
        return files_sorted
        
    except Exception as e:
        logger.error(f"Error listing files in {folder}: {e}")
        return []