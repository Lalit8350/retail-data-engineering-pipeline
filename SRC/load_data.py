
import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

CSV_PATH = PROJECT_ROOT / "data" / "processed" / "retail_cleaned.csv"

COLUMNS = [
    "invoice_no",
    "stock_code",
    "description",
    "quantity",
    "invoice_date",
    "unit_price",
    "customer_id",
    "country",
    "is_cancellation",
    "has_missing_customer_id",
    "has_missing_description",
    "has_non_positive_quantity",
    "has_non_positive_unit_price",
    "line_amount",
]


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Cleaned CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

  # Map CSV column names to PostgreSQL column names.
    COLUMN_MAPPING = {
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Country": "country",
    "IsCancellation": "is_cancellation",
    "HasMissingCustomerID": "has_missing_customer_id",
    "HasMissingDescription": "has_missing_description",
    "HasNonPositiveQuantity": "has_non_positive_quantity",
    "HasNonPositiveUnitPrice": "has_non_positive_unit_price",
    "LineAmount": "line_amount",
}

    df = df.rename(columns=COLUMN_MAPPING)
    # Convert customer IDs to nullable integers.
    df["customer_id"] = (
    pd.to_numeric(df["customer_id"], errors="coerce")
    .astype("Int64")
)
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing columns: {sorted(missing)}")

    df = df[COLUMNS]

    expected_rows = len(df)
    print(f"CSV rows: {expected_rows:,}")

    # Convert pandas missing values to Python None for PostgreSQL.
    df = df.astype(object).where(pd.notna(df), None)
    records = list(df.itertuples(index=False, name=None))

    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TEMP TABLE retail_transactions_staging
                (LIKE public.retail_transactions INCLUDING DEFAULTS)
                ON COMMIT DROP;
            """)

            insert_sql = """
                INSERT INTO retail_transactions_staging (
                    invoice_no, stock_code, description, quantity,
                    invoice_date, unit_price, customer_id, country,
                    is_cancellation, has_missing_customer_id,
                    has_missing_description, has_non_positive_quantity,
                    has_non_positive_unit_price, line_amount
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

            with cur.copy("""
                COPY retail_transactions_staging (
                    invoice_no, stock_code, description, quantity,
                    invoice_date, unit_price, customer_id, country,
                    is_cancellation, has_missing_customer_id,
                    has_missing_description, has_non_positive_quantity,
                    has_non_positive_unit_price, line_amount
                ) FROM STDIN
            """) as copy:
                for record in records:
                    copy.write_row(record)

            cur.execute("SELECT COUNT(*) FROM retail_transactions_staging")
            staged_rows = cur.fetchone()[0]

            if staged_rows != expected_rows:
                raise ValueError(
                    f"Row-count mismatch: expected {expected_rows}, "
                    f"staged {staged_rows}"
                )

            # Replace the target only after the staging count passes.
            cur.execute("DELETE FROM public.retail_transactions")

            cur.execute("""
                INSERT INTO public.retail_transactions (
                    invoice_no, stock_code, description, quantity,
                    invoice_date, unit_price, customer_id, country,
                    is_cancellation, has_missing_customer_id,
                    has_missing_description, has_non_positive_quantity,
                    has_non_positive_unit_price, line_amount
                )
                SELECT
                    invoice_no, stock_code, description, quantity,
                    invoice_date, unit_price, customer_id, country,
                    is_cancellation, has_missing_customer_id,
                    has_missing_description, has_non_positive_quantity,
                    has_non_positive_unit_price, line_amount
                FROM retail_transactions_staging
            """)

            cur.execute("SELECT COUNT(*) FROM public.retail_transactions")
            final_rows = cur.fetchone()[0]

            if final_rows != expected_rows:
                raise ValueError(
                    f"Final row-count mismatch: expected {expected_rows}, "
                    f"found {final_rows}"
                )

        # The transaction commits automatically if the block succeeds.
        # If an exception occurs, psycopg rolls it back.

    print(f"Load successful: {final_rows:,} rows loaded into PostgreSQL.")


if __name__ == "__main__":
    main()
