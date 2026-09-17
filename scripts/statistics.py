import pandas as pd
import numpy as np
from pathlib import Path


OUTPUT_DIR = Path("outputs/tables")


def run_statistics(df):
    print("\n[5/8] Statistical Analysis")
    print("=" * 50)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df = df.copy()

    # --------------------------------------------------
    # 1. Overall descriptive statistics
    # --------------------------------------------------
    print("\n1. OVERALL CRIME STATISTICS")

    crimes = df["crimes"]

    descriptive = crimes.describe()

    print(descriptive)

    stats_table = pd.DataFrame({
        "metric": [
            "count",
            "mean",
            "median",
            "std",
            "min",
            "25%",
            "50%",
            "75%",
            "max"
        ],
        "value": [
            crimes.count(),
            crimes.mean(),
            crimes.median(),
            crimes.std(),
            crimes.min(),
            crimes.quantile(0.25),
            crimes.quantile(0.50),
            crimes.quantile(0.75),
            crimes.max()
        ]
    })

    stats_table.to_csv(
        OUTPUT_DIR / "descriptive_statistics.csv",
        index=False
    )

    # --------------------------------------------------
    # 2. Variance
    # --------------------------------------------------
    print("\n2. VARIANCE")

    variance = crimes.var()

    print(f"Variance: {variance:,.2f}")

    # --------------------------------------------------
    # 3. Skewness
    # --------------------------------------------------
    print("\n3. SKEWNESS")

    skewness = crimes.skew()

    print(f"Skewness: {skewness:,.4f}")

    if skewness > 1:
        interpretation = "Highly right-skewed"
    elif skewness > 0.5:
        interpretation = "Moderately right-skewed"
    elif skewness < -1:
        interpretation = "Highly left-skewed"
    elif skewness < -0.5:
        interpretation = "Moderately left-skewed"
    else:
        interpretation = "Approximately symmetric"

    print(f"Distribution: {interpretation}")

    # --------------------------------------------------
    # 4. Interquartile Range
    # --------------------------------------------------
    print("\n4. INTERQUARTILE RANGE")

    q1 = crimes.quantile(0.25)
    q3 = crimes.quantile(0.75)

    iqr = q3 - q1

    print(f"Q1 : {q1:,.2f}")
    print(f"Q3 : {q3:,.2f}")
    print(f"IQR: {iqr:,.2f}")

    # --------------------------------------------------
    # 5. Outlier detection using IQR
    # --------------------------------------------------
    print("\n5. OUTLIER DETECTION")

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    outliers = df[
        (df["crimes"] < lower_bound) |
        (df["crimes"] > upper_bound)
    ]

    print(f"Lower bound : {lower_bound:,.2f}")
    print(f"Upper bound : {upper_bound:,.2f}")
    print(f"Outlier rows: {len(outliers):,}")

    if len(outliers) > 0:
        outliers[
            [
                "date",
                "state",
                "district",
                "category",
                "type",
                "crimes"
            ]
        ].to_csv(
            OUTPUT_DIR / "crime_outliers.csv",
            index=False
        )

    # --------------------------------------------------
    # 6. Statistics by state
    # --------------------------------------------------
    print("\n6. STATISTICS BY STATE")

    state_stats = (
        df.groupby("state")["crimes"]
        .agg(
            count="count",
            total="sum",
            mean="mean",
            median="median",
            std="std",
            minimum="min",
            maximum="max"
        )
        .reset_index()
    )

    print(
        state_stats
        .sort_values("total", ascending=False)
        .to_string(index=False)
    )

    state_stats.to_csv(
        OUTPUT_DIR / "statistics_by_state.csv",
        index=False
    )

    # --------------------------------------------------
    # 7. Statistics by category
    # --------------------------------------------------
    print("\n7. STATISTICS BY CATEGORY")

    category_stats = (
        df.groupby("category")["crimes"]
        .agg(
            count="count",
            total="sum",
            mean="mean",
            median="median",
            std="std",
            minimum="min",
            maximum="max"
        )
        .reset_index()
    )

    print(
        category_stats
        .sort_values("total", ascending=False)
        .to_string(index=False)
    )

    category_stats.to_csv(
        OUTPUT_DIR / "statistics_by_category.csv",
        index=False
    )

    # --------------------------------------------------
    # 8. Yearly statistics
    # --------------------------------------------------
    print("\n8. YEARLY STATISTICS")

    df["year"] = df["date"].dt.year

    yearly_stats = (
        df.groupby("year")["crimes"]
        .agg(
            total="sum",
            mean="mean",
            median="median",
            std="std",
            minimum="min",
            maximum="max"
        )
        .reset_index()
    )

    print(
        yearly_stats.to_string(index=False)
    )

    yearly_stats.to_csv(
        OUTPUT_DIR / "yearly_statistics.csv",
        index=False
    )

    # --------------------------------------------------
    # 9. Coefficient of variation
    # --------------------------------------------------
    print("\n9. COEFFICIENT OF VARIATION")

    mean_value = crimes.mean()
    std_value = crimes.std()

    if mean_value != 0:
        cv = (std_value / mean_value) * 100
    else:
        cv = np.nan

    print(f"Coefficient of Variation: {cv:,.2f}%")

    # --------------------------------------------------
    # Final summary
    # --------------------------------------------------
    print("\nSTATISTICAL SUMMARY")
    print("-" * 40)

    print(f"Mean       : {mean_value:,.2f}")
    print(f"Median     : {crimes.median():,.2f}")
    print(f"Std Dev    : {std_value:,.2f}")
    print(f"Variance   : {variance:,.2f}")
    print(f"Skewness   : {skewness:,.4f}")
    print(f"IQR        : {iqr:,.2f}")
    print(f"Outliers   : {len(outliers):,}")

    print("\n      ✓ Statistical analysis completed")

    return df