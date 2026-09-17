import pandas as pd
from pathlib import Path


PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "crime_district_clean.parquet"


def clean_data(df):
    print("\n[3/8] Data Cleaning")
    print("=" * 50)

    df = df.copy()

    # --------------------------------------------------
    # 1. Standardise column names
    # --------------------------------------------------
    print("\n1. Standardising column names")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("      ✓ Column names standardised")

    # --------------------------------------------------
    # 2. Convert date
    # --------------------------------------------------
    print("\n2. Converting date")

    if "date" in df.columns:
        original_invalid = df["date"].isna().sum()

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        invalid_dates = df["date"].isna().sum()

        print(f"      Invalid dates after conversion: {invalid_dates:,}")

        if invalid_dates > original_invalid:
            print("      ⚠ New invalid dates were detected")

        print("      ✓ Date converted to datetime")

    # --------------------------------------------------
    # 3. Clean text columns
    # --------------------------------------------------
    print("\n3. Standardising text columns")

    text_columns = [
        "state",
        "district",
        "category",
        "type"
    ]

    for column in text_columns:
        if column in df.columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )

            # Convert empty strings to missing values
            df[column] = df[column].replace("", pd.NA)

            print(f"      ✓ {column} cleaned")

    # --------------------------------------------------
    # 4. Check missing values
    # --------------------------------------------------
    print("\n4. Checking missing values")

    missing = df.isnull().sum()

    total_missing = missing.sum()

    print(f"      Total missing values: {total_missing:,}")

    for column, count in missing.items():
        if count > 0:
            print(f"      - {column}: {count:,}")

    # --------------------------------------------------
    # 5. Convert crimes to numeric
    # --------------------------------------------------
    print("\n5. Converting crimes to numeric")

    if "crimes" in df.columns:

        df["crimes"] = pd.to_numeric(
            df["crimes"],
            errors="coerce"
        )

        invalid_crimes = df["crimes"].isna().sum()

        print(
            f"      Invalid/missing crime values: "
            f"{invalid_crimes:,}"
        )

        print("      ✓ Crimes converted to numeric")

    # --------------------------------------------------
    # 6. Remove exact duplicate rows
    # --------------------------------------------------
    print("\n6. Checking duplicate rows")

    duplicates_before = df.duplicated().sum()

    print(
        f"      Duplicate rows found: "
        f"{duplicates_before:,}"
    )

    if duplicates_before > 0:
        df = df.drop_duplicates()
        print(
            f"      ✓ Removed {duplicates_before:,} "
            f"exact duplicate rows"
        )
    else:
        print("      ✓ No exact duplicate rows")

    # --------------------------------------------------
    # 7. Validate crime values
    # --------------------------------------------------
    print("\n7. Validating crime values")

    if "crimes" in df.columns:

        negative_crimes = (df["crimes"] < 0).sum()

        print(
            f"      Negative crime values: "
            f"{negative_crimes:,}"
        )

        if negative_crimes > 0:
            raise ValueError(
                "Negative crime values detected. "
                "Review the dataset before continuing."
            )

        print("      ✓ Crime values validated")

    # --------------------------------------------------
    # 8. Remove rows with critical missing values
    # --------------------------------------------------
    print("\n8. Handling critical missing values")

    critical_columns = [
        "date",
        "state",
        "district",
        "category",
        "type",
        "crimes"
    ]

    available_critical_columns = [
        column
        for column in critical_columns
        if column in df.columns
    ]

    rows_before = len(df)

    df = df.dropna(
        subset=available_critical_columns
    )

    rows_removed = rows_before - len(df)

    print(
        f"      Rows removed due to critical "
        f"missing values: {rows_removed:,}"
    )

    print("      ✓ Missing critical records handled")

    # --------------------------------------------------
    # 9. Sort data
    # --------------------------------------------------
    print("\n9. Sorting dataset")

    sort_columns = [
        column
        for column in ["date", "state", "district", "category", "type"]
        if column in df.columns
    ]

    df = df.sort_values(
        by=sort_columns
    ).reset_index(drop=True)

    print("      ✓ Dataset sorted")

    # --------------------------------------------------
    # 10. Save cleaned Parquet
    # --------------------------------------------------
    print("\n10. Saving cleaned dataset")

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        OUTPUT_FILE,
        index=False,
        engine="fastparquet"
    )

    print(
        f"      ✓ Saved: {OUTPUT_FILE}"
    )

    # --------------------------------------------------
    # Final summary
    # --------------------------------------------------
    print("\nCLEANING SUMMARY")
    print("-" * 40)

    print(f"Rows after cleaning    : {len(df):,}")
    print(f"Columns                : {len(df.columns)}")
    print(
        f"Missing values         : "
        f"{df.isnull().sum().sum():,}"
    )
    print(
        f"Duplicate rows         : "
        f"{df.duplicated().sum():,}"
    )

    print("\n      ✓ Data cleaning completed")

    return df