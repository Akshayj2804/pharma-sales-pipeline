from sqlalchemy import create_engine
import psycopg2
from psycopg2.extras import execute_values


def get_connection(db_url):
    return psycopg2.connect(db_url)


def insert_ignore(conn, df, table_name, columns):
    if df.empty:
        print(f"Skipping {table_name}, no data.")
        return

    df = df.drop_duplicates()

    values = [tuple(x) for x in df[columns].to_numpy()]

    cols = ",".join(columns)

    query = f"""
        INSERT INTO {table_name} ({cols})
        VALUES %s
        ON CONFLICT DO NOTHING
    """

    with conn.cursor() as cur:
        execute_values(cur, query, values)
        conn.commit()

    print(f"Loaded {len(values)} rows into {table_name}")


def load_all(customers, products, sales_team, fact, db_url):
    conn = get_connection(db_url)

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

    insert_ignore(
        conn,
        fact,
        "sales_fact",
        ["customer_name", "product_name", "quantity", "price", "sales", "year", "month"]
    )

    conn.close()