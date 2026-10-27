import pandas as pd
from pathlib import Path

# 1. Read the raw dataset
input_file = "data/raw/Online Retail.xlsx"
output_file = "data/processed/retail_cleaned.csv"

df = pd.read_excel(input_file)
print("\nMISSING VALUES AFTER STANDARDIZATION")
print(df.isna().sum())

print("Original row count:", len(df))

# 2. Remove exact duplicate rows
df = df.drop_duplicates().copy()

print("Rows after removing exact duplicates:", len(df))

# 3. Standardize text fields without inventing missing values
df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
df["StockCode"] = df["StockCode"].astype(str).str.strip()
df["Description"] = df["Description"].str.strip()
df["Description"] = df["Description"].replace("", pd.NA)

df["Country"] = df["Country"].str.strip()
df["Country"] = df["Country"].replace("", pd.NA)

# 4. Convert CustomerID to a nullable integer
df["CustomerID"] = pd.to_numeric(
    df["CustomerID"], errors="coerce"
).astype("Int64")

# 5. Add data-quality flags
df["IsCancellation"] = df["InvoiceNo"].str.startswith("C")
df["HasMissingCustomerID"] = df["CustomerID"].isna()
df["HasMissingDescription"] = df["Description"].isna()
df["HasNonPositiveQuantity"] = df["Quantity"] <= 0
df["HasNonPositiveUnitPrice"] = df["UnitPrice"] <= 0

# 6. Calculate line amount
df["LineAmount"] = df["Quantity"] * df["UnitPrice"]

# 7. Save processed data
Path("data/processed").mkdir(parents=True, exist_ok=True)

df.to_csv(output_file, index=False)

# 8. Validate the output
saved_df = pd.read_csv(output_file)

print("\nTRANSFORMATION SUMMARY")
print("Rows saved:", len(saved_df))
print("Columns saved:", len(saved_df.columns))
print("Cancellation rows:", saved_df["IsCancellation"].sum())
print("Missing customer IDs:", saved_df["HasMissingCustomerID"].sum())
print("Missing descriptions:", saved_df["HasMissingDescription"].sum())
print("Non-positive quantities:", saved_df["HasNonPositiveQuantity"].sum())
print("Non-positive unit prices:", saved_df["HasNonPositiveUnitPrice"].sum())
print("Output file:", output_file)

assert len(saved_df) == len(df), "Row count validation failed!"

print("\nPipeline completed successfully.")