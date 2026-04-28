from sqlalchemy import create_engine
import psycopg2
from psycopg2.extras import execute_values
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_connection(db_url):
    """
    Create PostgreSQL connection.
    
    Args:
        db_url: Database connection string
        
    Returns:
        psycopg2 connection object
    """
    try:
        conn = psycopg2.connect(db_url)
        logger.info("✓ Database connection established")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise


def insert_ignore(conn, df, table_name, columns):
    """
    Insert data into PostgreSQL table with ON CONFLICT DO NOTHING.
    
    Args:
        conn: Database connection
        df: DataFrame to insert
        table_name: Target table name
        columns: List of column names
    """
    try:
        if df.empty:
            logger.warning(f"Skipping {table_name}, no data to insert.")
            return
        
        # Remove duplicates before inserting
        df = df.drop_duplicates(subset=columns)
        
        # Convert to list of tuples
        values = [tuple(x) for x in df[columns].to_numpy()]
        
        # Build query
        cols = ", ".join(columns)
        query = f"""
            INSERT INTO {table_name} ({cols})
            VALUES %s
            ON CONFLICT DO NOTHING
        """
        
        # Execute batch insert
        with conn.cursor() as cur:
            execute_values(cur, query, values)
            conn.commit()
        
        logger.info(f"✓ Loaded {len(values)} rows into {table_name}")
        
    except Exception as e:
        logger.error(f"Error inserting into {table_name}: {e}")
        conn.rollback()
        raise


def load_all(customers, products, sales_team, fact, db_url):
    """
    Load all dimension and fact tables to PostgreSQL.
    
    Args:
        customers: Customer dimension DataFrame
        products: Product dimension DataFrame
        sales_team: Sales team dimension DataFrame
        fact: Sales fact DataFrame
        db_url: Database connection string
    """
    conn = None
    try:
        logger.info("Starting data load process...")
        
        # Establish connection
        conn = get_connection(db_url)
        
        # Load dimensions first
        insert_ignore(
            conn,
            customers,
            "customers_dim",
            ["customer_name", "city", "country"]
        )
        
        insert_ignore(
            conn,
            products,
            "products_dim",
            ["product_name", "product_class"]
        )
        
        insert_ignore(
            conn,
            sales_team,
            "sales_team_dim",
            ["name_of_sales_rep", "manager", "sales_team"]
        )
        
        # Load fact table
        insert_ignore(
            conn,
            fact,
            "sales_fact",
            ["customer_name", "product_name", "quantity", "price", "sales", "year", "month"]
        )
        
        logger.info("✓ All data loaded successfully")
        
    except Exception as e:
        logger.error(f"Error in load_all: {e}", exc_info=True)
        raise
        
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")