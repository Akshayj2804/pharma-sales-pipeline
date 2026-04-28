import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_schema(df):
    """
    Validate that all required columns are present.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame if valid
        
    Raises:
        ValueError if required columns are missing
    """
    required_columns = [
        "customer_name",
        "product_name",
        "quantity",
        "price",
        "sales",
        "year",
        "month"
    ]
    
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing:
        error_msg = f"Missing required columns: {missing}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("✓ Schema validation passed")
    return df


def validate_nulls(df):
    """
    Check for nulls in critical columns and log warnings.
    Drops rows with nulls in critical columns.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with null rows removed from critical columns
    """
    critical_cols = ["quantity", "price", "sales"]
    initial_count = len(df)
    
    for col in critical_cols:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            logger.warning(f"⚠️ Found {null_count} null values in '{col}' - removing these rows")
            df = df.dropna(subset=[col])
    
    dropped = initial_count - len(df)
    if dropped > 0:
        logger.warning(f"⚠️ Dropped {dropped} rows due to nulls in critical columns")
    else:
        logger.info("✓ No nulls found in critical columns")
    
    return df


def validate_ranges(df):
    """
    Validate that numeric columns are within acceptable ranges.
    Removes rows with invalid values.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with invalid rows removed
    """
    initial_count = len(df)
    
    # Remove negative or zero quantities
    invalid_qty = len(df[df["quantity"] <= 0])
    df = df[df["quantity"] > 0]
    if invalid_qty > 0:
        logger.warning(f"⚠️ Removed {invalid_qty} rows with quantity <= 0")
    
    # Remove negative or zero prices
    invalid_price = len(df[df["price"] <= 0])
    df = df[df["price"] > 0]
    if invalid_price > 0:
        logger.warning(f"⚠️ Removed {invalid_price} rows with price <= 0")
    
    # Remove negative sales
    invalid_sales = len(df[df["sales"] < 0])
    df = df[df["sales"] >= 0]
    if invalid_sales > 0:
        logger.warning(f"⚠️ Removed {invalid_sales} rows with sales < 0")
    
    total_dropped = initial_count - len(df)
    
    if total_dropped > 0:
        logger.warning(f"⚠️ Total rows dropped due to invalid ranges: {total_dropped}")
    else:
        logger.info("✓ Range validation passed")
    
    return df


def validate_data_quality(df):
    """
    Comprehensive data quality check.
    Logs statistics about the data.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame
    """
    logger.info(f"Data Quality Report:")
    logger.info(f"  - Total records: {len(df)}")
    logger.info(f"  - Unique customers: {df['customer_name'].nunique()}")
    logger.info(f"  - Unique products: {df['product_name'].nunique()}")
    logger.info(f"  - Date range: {df['year'].min()}-{df['month'].min()} to {df['year'].max()}-{df['month'].max()}")
    logger.info(f"  - Total sales value: ${df['sales'].sum():,.2f}")
    logger.info(f"  - Average transaction: ${df['sales'].mean():,.2f}")
    
    return df