import pandas as pd


def understand_data(df):
    print("\n[2/8] Data Understanding")
    print("=" * 50)

    # Basic information
    print("\nDATASET SIZE")
    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]}")

    # Column names
    print("\nCOLUMNS")
    for column in df.columns:
        print(f" - {column}")

    # Data types
    print("\nDATA TYPES")
    print(df.dtypes)

    # Missing values
    print("\nMISSING VALUES")
    missing = df.isnull().sum()

    for column, count in missing.items():
        print(f" - {column}: {count:,}")

    # Duplicate rows
    print("\nDUPLICATES")
    duplicates = df.duplicated().sum()
    print(f"Duplicate rows: {duplicates:,}")

    # Date information
    if "date" in df.columns:
        dates = pd.to_datetime(df["date"], errors="coerce")

        print("\nDATE RANGE")
        print(f"Start: {dates.min()}")
        print(f"End  : {dates.max()}")

    # Unique values
    for column in ["state", "district", "category", "type"]:
        if column in df.columns:
            print(f"\nUNIQUE {column.upper()}")
            print(f"Count: {df[column].nunique():,}")

            values = df[column].dropna().unique()

            for value in values[:20]:
                print(f" - {value}")

            if len(values) > 20:
                print(f" ... and {len(values) - 20:,} more")

    # Numerical summary
    print("\nCRIME STATISTICS")

    if "crimes" in df.columns:
        print(df["crimes"].describe())

    print("\n      ✓ Data understanding completed")

    return df