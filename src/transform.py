import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_columns(df):
    """
    Standardize column names: lowercase, strip whitespace, replace spaces with underscores.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with cleaned column names
    """
    try:
        original_cols = df.columns.tolist()
        
        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(r"^\w\s", "", regex=True)
            .str.replace(r"\s", "_", regex=True)
        )
        
        logger.info(f"✓ Cleaned {len(df.columns)} column names")
        return df
        
    except Exception as e:
        logger.error(f"Error cleaning columns: {e}")
        raise


def convert_types(df):
    """
    Convert columns to appropriate data types with validation.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with converted types
    """
    try:
        initial_count = len(df)
        
        # Convert numeric columns
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
        
        # Convert year and month
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
        df["month"] = pd.to_numeric(df["month"], errors="coerce").astype("Int64")
        
        # Check for conversion failures
        qty_nulls = df["quantity"].isnull().sum()
        price_nulls = df["price"].isnull().sum()
        
        if qty_nulls > 0:
            logger.warning(f"⚠️ {qty_nulls} rows failed quantity conversion")
        if price_nulls > 0:
            logger.warning(f"⚠️ {price_nulls} rows failed price conversion")
        
        # Remove rows with invalid conversions
        df = df.dropna(subset=["quantity", "price", "sales"])
        
        # Validate month range
        df = df[(df["month"] >= 1) & (df["month"] <= 12)]
        
        dropped = initial_count - len(df)
        if dropped > 0:
            logger.warning(f"⚠️ Dropped {dropped} rows during type conversion")
        
        logger.info("✓ Type conversion completed")
        return df
        
    except Exception as e:
        logger.error(f"Error converting types: {e}")
        raise


def business_logic(df):
    """
    Apply business rules and calculations.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with business logic applied
    """
    try:
        # Recalculate sales (price * quantity)
        df["sales"] = df["price"] * df["quantity"]
        
        logger.info("✓ Business logic applied")
        return df
        
    except Exception as e:
        logger.error(f"Error applying business logic: {e}")
        raise


def remove_duplicates(df):
    """
    Remove duplicate rows and log count.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with duplicates removed
    """
    try:
        initial_count = len(df)
        df = df.drop_duplicates()
        duplicates = initial_count - len(df)
        
        if duplicates > 0:
            logger.warning(f"⚠️ Removed {duplicates} duplicate rows")
        else:
            logger.info("✓ No duplicates found")
        
        return df
        
    except Exception as e:
        logger.error(f"Error removing duplicates: {e}")
        raise


def transform_data(df):
    """
    Main transformation pipeline.
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Transformed DataFrame
    """
    try:
        logger.info("Starting data transformation...")
        initial_count = len(df)
        
        df = clean_columns(df)
        df = convert_types(df)
        df = business_logic(df)
        df = remove_duplicates(df)
        
        final_count = len(df)
        logger.info(f"Transformation complete: {initial_count} → {final_count} records")
        
        return df
        
    except Exception as e:
        logger.error(f"Error in transformation pipeline: {e}", exc_info=True)
        raise