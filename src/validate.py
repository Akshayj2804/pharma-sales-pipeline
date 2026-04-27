def validate_schema(df):
    required_columns = [
        "customer_name",
        "product_name",
        "quantity",
        "price",
        "sales",
        "year",
        "month"
    ]

    missing =[col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Mission columns: {missing}")
    
    return df

def validate_nulls(df):
    critical_col = ["quantity","price","sales"]

    for col in critical_col:
        if df[col].isnull().sum() > 0:
            print(f"Warning: Nulls found in {col}")

        return df
    
def validate_ranges(df):
    df = df[df["quantity"] > 0]
    df = df[df["price"] > 0]
    df = df[df["sales"] >= 0]

    return df
