from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
import os

#  tell Airflow where the project is
sys.path.append("/mnt/c/Users/dell/Projects/sales-data-pipeline")

# import your pipeline modules
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


# 🎯 MAIN PIPELINE FUNCTION (this is what Airflow runs)
def run_pipeline():

    # STEP 1: Extract next file
    df, file = extract_next_batch()

    if df is None:
        print("No new data. Skipping run.")
        return

    print(f"Processing file: {file}")

    # STEP 2: Validate
    df = validate_schema(df)
    df = validate_nulls(df)
    df = validate_ranges(df)

    # STEP 3: Transform
    df = transform_data(df)

    # STEP 4: Model
    customers = create_customers_dim(df)
    products = create_products_dim(df)
    sales_team = create_sales_team_dim(df)
    fact = create_fact_table(df)

    # STEP 5: Load
    load_all(customers, products, sales_team, fact, DB_URL)

    # STEP 6: Update checkpoint
    update_checkpoint(file)

    print(f"Finished processing: {file}")


# 🧱 DAG DEFAULT CONFIG
default_args = {
    "owner": "akki",
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}


# 🧱 DAG DEFINITION
with DAG(
    dag_id="sales_pipeline",
    default_args=default_args,
    schedule="@daily",   # runs daily
    catchup=False        # don't run old dates
) as dag:

    # 🎯 TASK (only one for now)
    run_etl = PythonOperator(
        task_id="run_pipeline",
        python_callable=run_pipeline
    )

    run_etl