import pandas as pd
from pathlib import Path


OUTPUT_DIR = Path("outputs/tables")


def run_pattern_analysis(df):
    print("\n[6/8] Pattern Analysis")
    print("=" * 50)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df = df.copy()

    # --------------------------------------------------
    # Prepare year
    # --------------------------------------------------
    df["year"] = df["date"].dt.year

    # ==================================================
    # 1. YEAR-OVER-YEAR CHANGE
    # ==================================================
    print("\n1. YEAR-OVER-YEAR CRIME CHANGE")

    yearly = (
        df.groupby("year")["crimes"]
        .sum()
        .reset_index()
    )

    yearly["change"] = yearly["crimes"].diff()

    yearly["percentage_change"] = (
        yearly["crimes"]
        .pct_change()
        .mul(100)
    )

    print(yearly.to_string(index=False))

    yearly.to_csv(
        OUTPUT_DIR / "year_over_year_change.csv",
        index=False
    )

    # ==================================================
    # 2. CATEGORY SHARE
    # ==================================================
    print("\n2. CRIME SHARE BY CATEGORY")

    category = (
        df.groupby("category")["crimes"]
        .sum()
        .reset_index()
    )

    total_crimes = category["crimes"].sum()

    category["percentage_share"] = (
        category["crimes"] /
        total_crimes *
        100
    )

    category = category.sort_values(
        "percentage_share",
        ascending=False
    )

    print(category.to_string(index=False))

    category.to_csv(
        OUTPUT_DIR / "category_crime_share.csv",
        index=False
    )

    # ==================================================
    # 3. CATEGORY TREND
    # ==================================================
    print("\n3. CATEGORY TREND OVER TIME")

    category_trend = (
        df.groupby(
            ["year", "category"]
        )["crimes"]
        .sum()
        .reset_index()
    )

    category_trend["yearly_change"] = (
        category_trend
        .groupby("category")["crimes"]
        .diff()
    )

    category_trend["percentage_change"] = (
        category_trend
        .groupby("category")["crimes"]
        .pct_change()
        .mul(100)
    )

    print(
        category_trend
        .tail(20)
        .to_string(index=False)
    )

    category_trend.to_csv(
        OUTPUT_DIR / "category_trend.csv",
        index=False
    )

    # ==================================================
    # 4. STATE TREND
    # ==================================================
    print("\n4. STATE TREND OVER TIME")

    state_trend = (
        df.groupby(
            ["year", "state"]
        )["crimes"]
        .sum()
        .reset_index()
    )

    state_trend["yearly_change"] = (
        state_trend
        .groupby("state")["crimes"]
        .diff()
    )

    state_trend["percentage_change"] = (
        state_trend
        .groupby("state")["crimes"]
        .pct_change()
        .mul(100)
    )

    print(
        state_trend
        .sort_values("crimes", ascending=False)
        .head(20)
        .to_string(index=False)
    )

    state_trend.to_csv(
        OUTPUT_DIR / "state_trend.csv",
        index=False
    )

    # ==================================================
    # 5. STATE × CATEGORY
    # ==================================================
    print("\n5. STATE × CATEGORY PATTERNS")

    state_category = (
        df.groupby(
            ["state", "category"]
        )["crimes"]
        .sum()
        .reset_index()
    )

    state_category["state_share"] = (
        state_category
        .groupby("state")["crimes"]
        .transform("sum")
    )

    state_category["percentage_within_state"] = (
        state_category["crimes"] /
        state_category["state_share"] *
        100
    )

    state_category = state_category.drop(
        columns=["state_share"]
    )

    print(
        state_category
        .sort_values("crimes", ascending=False)
        .head(30)
        .to_string(index=False)
    )

    state_category.to_csv(
        OUTPUT_DIR / "state_category_patterns.csv",
        index=False
    )

    # ==================================================
    # 6. HIGHEST YEARLY INCREASE
    # ==================================================
    print("\n6. HIGHEST YEARLY INCREASE")

    valid_changes = yearly.dropna(
        subset=["percentage_change"]
    )

    if not valid_changes.empty:

        highest_increase = valid_changes.loc[
            valid_changes["percentage_change"].idxmax()
        ]

        highest_decrease = valid_changes.loc[
            valid_changes["percentage_change"].idxmin()
        ]

        print(
            f"Highest increase: "
            f"{highest_increase['year']} "
            f"({highest_increase['percentage_change']:.2f}%)"
        )

        print(
            f"Highest decrease: "
            f"{highest_decrease['year']} "
            f"({highest_decrease['percentage_change']:.2f}%)"
        )

    # ==================================================
    # 7. MOST DOMINANT CATEGORY PER STATE
    # ==================================================
    print("\n7. DOMINANT CATEGORY WITHIN EACH STATE")

    dominant_category = (
        state_category.loc[
            state_category
            .groupby("state")["crimes"]
            .idxmax()
        ]
        .sort_values("state")
        .reset_index(drop=True)
    )

    print(
        dominant_category[
            [
                "state",
                "category",
                "crimes",
                "percentage_within_state"
            ]
        ].to_string(index=False)
    )

    dominant_category.to_csv(
        OUTPUT_DIR / "dominant_category_by_state.csv",
        index=False
    )

    # ==================================================
    # 8. CONSISTENCY ANALYSIS
    # ==================================================
    print("\n8. CATEGORY CONSISTENCY")

    category_consistency = (
        category_trend
        .groupby("category")["crimes"]
        .agg(
            mean="mean",
            std="std",
            minimum="min",
            maximum="max"
        )
        .reset_index()
    )

    category_consistency["coefficient_of_variation"] = (
        category_consistency["std"] /
        category_consistency["mean"]
    )

    print(
        category_consistency
        .sort_values(
            "coefficient_of_variation",
            ascending=False
        )
        .to_string(index=False)
    )

    category_consistency.to_csv(
        OUTPUT_DIR / "category_consistency.csv",
        index=False
    )

    # ==================================================
    # FINAL SUMMARY
    # ==================================================
    print("\nPATTERN ANALYSIS SUMMARY")
    print("-" * 40)

    print(
        f"Years analysed      : "
        f"{df['year'].nunique():,}"
    )

    print(
        f"States analysed     : "
        f"{df['state'].nunique():,}"
    )

    print(
        f"Categories analysed: "
        f"{df['category'].nunique():,}"
    )

    print(
        "\n      ✓ Pattern analysis completed"
    )

    return df