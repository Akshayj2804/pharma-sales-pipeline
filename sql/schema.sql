DROP TABLE IF EXISTS customers_dim;
DROP TABLE IF EXISTS products_dim;
DROP TABLE IF EXISTS sales_team_dim;
DROP TABLE IF EXISTS sales_fact;

CREATE TABLE customers_dim (
    customer_id SERIAL PRIMARY KEY,
    customer_name TEXT,
    city TEXT,
    country TEXT,
    UNIQUE (customer_name, city, country)
);

CREATE TABLE products_dim (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT,
    product_class TEXT,
    UNIQUE (product_name, product_class)
);

CREATE TABLE sales_team_dim (
    sales_team_id SERIAL PRIMARY KEY,
    name_of_sales_rep TEXT,
    manager TEXT,
    sales_team TEXT,
    UNIQUE (name_of_sales_rep, manager, sales_team)
);

CREATE TABLE sales_fact (
    customer_name TEXT,
    product_name TEXT,
    quantity INT,
    price FLOAT,
    sales FLOAT,
    year INT,
    month INT,
    UNIQUE (customer_name, product_name, year, month)
);