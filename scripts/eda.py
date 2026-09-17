import pandas as pd
from pathlib import Path


OUTPUT_DIR = Path("outputs/tables")


def run_eda(df):
    print("\n[4/8] Exploratory Data Analysis")
    print("=" * 50)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------
    # Prepare year
    # --------------------------------------------------
    df = df.copy()

    df["year"] = df["date"].dt.year

    # --------------------------------------------------
    # 1. Yearly crime trend
    # --------------------------------------------------
    print("\n1. CRIME TREND BY YEAR")

    yearly_crimes = (
        df.groupby("year")["crimes"]
        .sum()
        .reset_index()
    )

    print(yearly_crimes.to_string(index=False))

    yearly_crimes.to_csv(
        OUTPUT_DIR / "crime_by_year.csv",
        index=False
    )

    # --------------------------------------------------
    # 2. Crime by state
    # --------------------------------------------------
    print("\n2. TOTAL CRIMES BY STATE")

    state_crimes = (
        df.groupby("state")["crimes"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    print(state_crimes.to_string(index=False))

    state_crimes.to_csv(
        OUTPUT_DIR / "crime_by_state.csv",
        index=False
    )

    # --------------------------------------------------
    # 3. Crime by category
    # --------------------------------------------------
    print("\n3. TOTAL CRIMES BY CATEGORY")

    category_crimes = (
        df.groupby("category")["crimes"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    print(category_crimes.to_string(index=False))

    category_crimes.to_csv(
        OUTPUT_DIR / "crime_by_category.csv",
        index=False
    )

    # --------------------------------------------------
    # 4. Crime by type
    # --------------------------------------------------
    print("\n4. TOTAL CRIMES BY TYPE")

    type_crimes = (
        df.groupby("type")["crimes"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    print(type_crimes.head(20).to_string(index=False))

    type_crimes.to_csv(
        OUTPUT_DIR / "crime_by_type.csv",
        index=False
    )

    # --------------------------------------------------
    # 5. Top police districts
    # --------------------------------------------------
    print("\n5. TOP 20 POLICE DISTRICTS")

    district_crimes = (
        df.groupby("district")["crimes"]
        .sum()
        .sort_values(ascending=False)
        .head(20)
        .reset_index()
    )

    print(district_crimes.to_string(index=False))

    district_crimes.to_csv(
        OUTPUT_DIR / "top_20_districts.csv",
        index=False
    )

    # --------------------------------------------------
    # 6. State × Category
    # --------------------------------------------------
    print("\n6. CRIME BY STATE AND CATEGORY")

    state_category = (
        df.groupby(
            ["state", "category"]
        )["crimes"]
        .sum()
        .reset_index()
    )

    print(
        state_category
        .sort_values("crimes", ascending=False)
        .head(20)
        .to_string(index=False)
    )

    state_category.to_csv(
        OUTPUT_DIR / "crime_state_category.csv",
        index=False
    )

    # --------------------------------------------------
    # 7. EDA summary
    # --------------------------------------------------
    print("\n7. EDA SUMMARY")

    print(f"Years analysed       : {df['year'].nunique():,}")
    print(f"States analysed      : {df['state'].nunique():,}")
    print(f"Districts analysed   : {df['district'].nunique():,}")
    print(f"Categories analysed  : {df['category'].nunique():,}")
    print(f"Crime types analysed : {df['type'].nunique():,}")

    print(
        f"Total recorded crimes: "
        f"{df['crimes'].sum():,.0f}"
    )

    print("\n      ✓ EDA completed")

    return df