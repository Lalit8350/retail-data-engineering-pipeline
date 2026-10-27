import pandas as pd
from pathlib import Path

OUTPUT_FILE = Path("data/processed/retail_cleaned.csv")


def test_output_file_exists():
    assert OUTPUT_FILE.exists(), "Processed CSV does not exist"


def test_row_count():
    df = pd.read_csv(OUTPUT_FILE)

    assert len(df) > 0, "Processed dataset is empty"
    assert len(df) <= 541909, "Processed rows exceed raw rows"

    print(f"Validated processed row count: {len(df)}")


def test_required_columns_exist():
    df = pd.read_csv(OUTPUT_FILE, nrows=5)

    required_columns = [
        "InvoiceNo",
        "StockCode",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
        "LineAmount",
        "IsCancellation",
    ]

    for column in required_columns:
        assert column in df.columns, f"Missing column: {column}"


def test_no_exact_duplicate_rows():
    df = pd.read_csv(OUTPUT_FILE)
    assert not df.duplicated().any(), "Duplicate rows remain"


def test_line_amount_calculation():
    df = pd.read_csv(OUTPUT_FILE, nrows=1000)

    expected = df["Quantity"] * df["UnitPrice"]

    assert (
        (df["LineAmount"] - expected).abs() < 0.000001
    ).all(), "LineAmount calculation is incorrect"


if __name__ == "__main__":
    tests = [
        test_output_file_exists,
        test_row_count,
        test_required_columns_exist,
        test_no_exact_duplicate_rows,
        test_line_amount_calculation,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nAll data-quality tests passed!")