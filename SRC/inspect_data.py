
import pandas as pd

file_path = "data/raw/Online Retail.xlsx"

df = pd.read_excel(file_path)

print("FIRST 5 ROWS")
print(df.head())

print("\nDATASET DIMENSIONS")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())

print("\nMISSING VALUES PER COLUMN")
print(df.isnull().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

print("\nDATA TYPES")
print(df.dtypes)

print("\nQUANTITY SUMMARY")
print(df["Quantity"].describe())

print("\nUNIT PRICE SUMMARY")
print(df["UnitPrice"].describe())

print("\nNON-POSITIVE QUANTITIES")
print((df["Quantity"] <= 0).sum())

print("\nZERO OR NEGATIVE PRICES")
print((df["UnitPrice"] <= 0).sum())

print("\nINVOICE NUMBERS STARTING WITH C")
print(df["InvoiceNo"].astype(str).str.startswith("C").sum())

print("\nDATE RANGE")
print("Earliest:", df["InvoiceDate"].min())
print("Latest:", df["InvoiceDate"].max())

print("\nSAMPLE NEGATIVE QUANTITIES")
print(
    df.loc[
        df["Quantity"] < 0,
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "CustomerID"]
    ].head(10).to_string(index=False)
)

print("\nSAMPLE ZERO-PRICE ROWS")
print(
    df.loc[
        df["UnitPrice"] == 0,
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice"]
    ].head(10).to_string(index=False)
)

print("\nSAMPLE NEGATIVE-PRICE ROWS")
print(
    df.loc[
        df["UnitPrice"] < 0,
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice"]
    ].head(10).to_string(index=False)
)

print("\nINVOICE PREFIX C: QUANTITY SUMMARY")
print(
    df.loc[
        df["InvoiceNo"].astype(str).str.startswith("C"),
        "Quantity"
    ].describe()
)