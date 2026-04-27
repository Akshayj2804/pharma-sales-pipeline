import pandas as pd

def clean_columns(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"^\w\s","", regex=True)
        .str.replace(r"\s","_", regex=True)
    )
    return df

def convert_types(df):
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["month"] = pd.to_numeric(df["month"], errors="coerce").astype("Int64")
    df = df[(df["month"] >= 1) & (df["month"] <= 12)]
    return df

def business_logic(df):
    df["sales"] = df["price"] * df["quantity"]

    return df

def remove_duplicates(df):
    return df.drop_duplicates()

def transform_data(df):
    df = clean_columns(df)
    df = convert_types(df)
    df = business_logic(df)
    df = remove_duplicates(df)

    return df