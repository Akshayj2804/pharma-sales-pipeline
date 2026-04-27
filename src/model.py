def create_customers_dim(df):
    return df[[
        "customer_name",
        "city",
        "country"
    ]].drop_duplicates()


def create_products_dim(df):
    return df[[
        "product_name",
        "product_class"
    ]].drop_duplicates()


def create_sales_team_dim(df):
    return df[[
        "name_of_sales_rep",
        "manager",
        "sales_team"
    ]].drop_duplicates()


def create_fact_table(df):
    return df[[
        "customer_name",
        "product_name",
        "quantity",
        "price",
        "sales",
        "year",
        "month"
    ]]