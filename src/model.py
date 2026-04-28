import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_customers_dim(df):
    """
    Create customer dimension table.
    
    Args:
        df: Transformed sales DataFrame
        
    Returns:
        Customer dimension DataFrame
    """
    try:
        customers = df[[
            "customer_name",
            "city",
            "country"
        ]].drop_duplicates()
        
        logger.info(f"✓ Created customers dimension: {len(customers)} unique customers")
        return customers
        
    except Exception as e:
        logger.error(f"Error creating customers dimension: {e}")
        raise


def create_products_dim(df):
    """
    Create product dimension table.
    
    Args:
        df: Transformed sales DataFrame
        
    Returns:
        Product dimension DataFrame
    """
    try:
        products = df[[
            "product_name",
            "product_class"
        ]].drop_duplicates()
        
        logger.info(f"✓ Created products dimension: {len(products)} unique products")
        return products
        
    except Exception as e:
        logger.error(f"Error creating products dimension: {e}")
        raise


def create_sales_team_dim(df):
    """
    Create sales team dimension table.
    
    Args:
        df: Transformed sales DataFrame
        
    Returns:
        Sales team dimension DataFrame
    """
    try:
        sales_team = df[[
            "name_of_sales_rep",
            "manager",
            "sales_team"
        ]].drop_duplicates()
        
        logger.info(f"✓ Created sales team dimension: {len(sales_team)} unique members")
        return sales_team
        
    except Exception as e:
        logger.error(f"Error creating sales team dimension: {e}")
        raise


def create_fact_table(df):
    """
    Create sales fact table.
    
    Args:
        df: Transformed sales DataFrame
        
    Returns:
        Sales fact DataFrame
    """
    try:
        fact = df[[
            "customer_name",
            "product_name",
            "quantity",
            "price",
            "sales",
            "year",
            "month"
        ]]
        
        logger.info(f"✓ Created fact table: {len(fact)} records")
        return fact
        
    except Exception as e:
        logger.error(f"Error creating fact table: {e}")
        raise