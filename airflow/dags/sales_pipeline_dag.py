"""
Pharmaceutical Sales Data Pipeline DAG

This DAG orchestrates an incremental batch processing pipeline that:
1. Extracts the next unprocessed parquet file
2. Validates data quality
3. Transforms and cleans the data
4. Models into fact and dimension tables
5. Loads into PostgreSQL
6. Updates checkpoint for next run

Runs daily and skips if no new data is available.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging

# Import pipeline functions
from src.extract import extract_next_batch, update_checkpoint
from src.validate import validate_schema, validate_nulls, validate_ranges
from src.transform import transform_data
from src.model import (
    create_customers_dim,
    create_products_dim,
    create_sales_team_dim,
    create_fact_table
)
from src.load import load_all
from config.config import DB_URL


logger = logging.getLogger(__name__)


def run_pipeline(**context):
    """
    Main pipeline execution function.
    
    Returns:
        str: Status message indicating success or skip
    
    Raises:
        Exception: If pipeline execution fails
    """
    try:
        # EXTRACT
        logger.info("Starting extraction phase...")
        result = extract_next_batch()
        
        if result is None:
            logger.info("No new data to process. Skipping pipeline execution.")
            return "SKIPPED: No new data available"
        
        df, file_name = result
        logger.info(f"Extracted {len(df)} records from {file_name}")
        
        # VALIDATE
        logger.info("Starting validation phase...")
        validate_schema(df)
        validate_nulls(df)
        validate_ranges(df)
        logger.info("Validation completed successfully")
        
        # TRANSFORM
        logger.info("Starting transformation phase...")
        df_transformed = transform_data(df)
        logger.info(f"Transformation completed. Records: {len(df_transformed)}")
        
        # MODEL
        logger.info("Starting data modeling phase...")
        customers_dim = create_customers_dim(df_transformed)
        products_dim = create_products_dim(df_transformed)
        sales_team_dim = create_sales_team_dim(df_transformed)
        fact_table = create_fact_table(df_transformed)
        
        logger.info(f"Modeling completed:")
        logger.info(f"  - Customers: {len(customers_dim)}")
        logger.info(f"  - Products: {len(products_dim)}")
        logger.info(f"  - Sales Team: {len(sales_team_dim)}")
        logger.info(f"  - Fact Records: {len(fact_table)}")
        
        # LOAD
        logger.info("Starting load phase...")
        load_all(customers_dim, products_dim, sales_team_dim, fact_table, DB_URL)
        logger.info("Data loaded successfully to PostgreSQL")
        
        # UPDATE CHECKPOINT
        logger.info(f"Updating checkpoint with file: {file_name}")
        update_checkpoint(file_name)
        
        logger.info(f"Pipeline completed successfully for {file_name}")
        return f"SUCCESS: Processed {file_name} with {len(fact_table)} fact records"
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)
        raise


# DAG default arguments
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}


# DAG definition
with DAG(
    dag_id='pharma_sales_pipeline',
    default_args=default_args,
    description='Incremental pharmaceutical sales data processing pipeline',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['etl', 'sales', 'pharma', 'incremental'],
) as dag:
    
    pipeline_task = PythonOperator(
        task_id='run_sales_pipeline',
        python_callable=run_pipeline,
        provide_context=True,
    )
    
    pipeline_task