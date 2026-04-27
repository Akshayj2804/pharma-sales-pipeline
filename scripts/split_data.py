import pandas as pd
import os

from config.config import RAW_DATA_PATH, RAW_FOLDER
from src.utils import ensure_dir

def split_csv_to_parquet():

    ensure_dir(RAW_FOLDER)

    df = pd.read_csv(RAW_DATA_PATH)

    # clean column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.replace(r"\s+", "_", regex=True)
    )

    # convert types
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    # df["month"] = pd.to_numeric(df["month"], errors="coerce").astype("Int64")
    df["month"] = pd.to_datetime(df["month"], format="%B", errors="coerce").dt.month
    df["month"] = df["month"].astype("Int64")
    

    # drop bad rows
    df = df.dropna(subset=["year", "month"])

    # create partition key
    df["year_month"] = (
        df["year"].astype(int).astype(str) + "_" +
        df["month"].astype(int).astype(str).str.zfill(2)
    )

    # split and save
    for ym, group in df.groupby("year_month"):
        file_path = os.path.join(RAW_FOLDER, f"{ym}.parquet")
        group.to_parquet(file_path, index=False)
        print(f"Saved: {file_path}")


if __name__ == "__main__":
    split_csv_to_parquet()