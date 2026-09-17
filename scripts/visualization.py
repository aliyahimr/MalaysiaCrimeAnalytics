import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


FIGURE_DIR = Path("outputs/figures")
TABLE_DIR = Path("outputs/tables")


def run_visualization(df):

    print("\n[8/8] Visualization")
    print("=" * 50)

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    df = df.copy()
    df["year"] = df["date"].dt.year

    # =========================================================
    # 1. CRIME TREND BY YEAR
    # =========================================================

    print("\n1. Creating yearly crime trend")

    yearly = (
        df.groupby("year")["crimes"]
        .sum()
        .reset_index()
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        yearly["year"],
        yearly["crimes"],
        marker="o"
    )

    plt.title("Recorded Crimes in Malaysia by Year")
    plt.xlabel("Year")
    plt.ylabel("Recorded Crimes")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "crime_trend_by_year.png",
        dpi=300
    )

    plt.close()

    print("      ✓ crime_trend_by_year.png")

    # =========================================================
    # 2. CRIME BY STATE
    # =========================================================

    print("\n2. Creating state crime comparison")

    state_crimes = (
        df.groupby("state")["crimes"]
        .sum()
        .sort_values(ascending=True)
    )

    plt.figure(figsize=(10, 8))

    state_crimes.plot(
        kind="barh"
    )

    plt.title("Total Recorded Crimes by State")
    plt.xlabel("Recorded Crimes")
    plt.ylabel("State")
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "crime_by_state.png",
        dpi=300
    )

    plt.close()

    print("      ✓ crime_by_state.png")

    # =========================================================
    # 3. CRIME BY CATEGORY
    # =========================================================

    print("\n3. Creating crime category comparison")

    category_crimes = (
        df.groupby("category")["crimes"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))

    category_crimes.plot(
        kind="bar"
    )

    plt.title("Total Recorded Crimes by Category")
    plt.xlabel("Crime Category")
    plt.ylabel("Recorded Crimes")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "crime_by_category.png",
        dpi=300
    )

    plt.close()

    print("      ✓ crime_by_category.png")

    # =========================================================
    # 4. TOP 20 POLICE DISTRICTS
    # =========================================================

    print("\n4. Creating top district comparison")

    district_crimes = (
        df.groupby("district")["crimes"]
        .sum()
        .sort_values(ascending=False)
        .head(20)
        .sort_values(ascending=True)
    )

    plt.figure(figsize=(10, 8))

    district_crimes.plot(
        kind="barh"
    )

    plt.title("Top 20 Police Districts by Recorded Crimes")
    plt.xlabel("Recorded Crimes")
    plt.ylabel("Police District")
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "top_20_districts.png",
        dpi=300
    )

    plt.close()

    print("      ✓ top_20_districts.png")

    # =========================================================
    # 5. CATEGORY TREND
    # =========================================================

    print("\n5. Creating category trend")

    category_trend = (
        df.groupby(["year", "category"])["crimes"]
        .sum()
        .reset_index()
    )

    plt.figure(figsize=(11, 7))

    for category in category_trend["category"].unique():

        subset = category_trend[
            category_trend["category"] == category
        ]

        plt.plot(
            subset["year"],
            subset["crimes"],
            marker="o",
            label=category
        )

    plt.title("Crime Category Trends Over Time")
    plt.xlabel("Year")
    plt.ylabel("Recorded Crimes")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "category_trends.png",
        dpi=300
    )

    plt.close()

    print("      ✓ category_trends.png")

    # =========================================================
    # 6. STATE × CATEGORY HEATMAP
    # =========================================================

    print("\n6. Creating state-category heatmap")

    state_category = (
        df.groupby(["state", "category"])["crimes"]
        .sum()
        .unstack(fill_value=0)
    )

    plt.figure(figsize=(12, 8))

    plt.imshow(
        state_category,
        aspect="auto"
    )

    plt.title("Recorded Crimes by State and Category")
    plt.xlabel("Crime Category")
    plt.ylabel("State")

    plt.xticks(
        range(len(state_category.columns)),
        state_category.columns,
        rotation=45,
        ha="right"
    )

    plt.yticks(
        range(len(state_category.index)),
        state_category.index
    )

    plt.colorbar(
        label="Recorded Crimes"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "state_category_heatmap.png",
        dpi=300
    )

    plt.close()

    print("      ✓ state_category_heatmap.png")

    # =========================================================
    # 7. CLUSTER DISTRIBUTION
    # =========================================================

    cluster_file = (
        TABLE_DIR / "district_clusters.csv"
    )

    if cluster_file.exists():

        print("\n7. Creating cluster distribution")

        clusters = pd.read_csv(
            cluster_file
        )

        cluster_counts = (
            clusters["cluster"]
            .value_counts()
            .sort_index()
        )

        plt.figure(figsize=(8, 6))

        cluster_counts.plot(
            kind="bar"
        )

        plt.title(
            "Number of Police Districts by Cluster"
        )

        plt.xlabel("Cluster")
        plt.ylabel("Number of Police Districts")

        plt.xticks(rotation=0)

        plt.tight_layout()

        plt.savefig(
            FIGURE_DIR / "cluster_distribution.png",
            dpi=300
        )

        plt.close()

        print("      ✓ cluster_distribution.png")

    else:

        print(
            "      ⚠ district_clusters.csv not found"
        )

    # =========================================================
    # 8. CLUSTER CRIME PROFILE
    # =========================================================

    if cluster_file.exists():

        print("\n8. Creating cluster crime profile")

        cluster_summary = (
            clusters
            .groupby("cluster")["total_crimes"]
            .mean()
        )

        plt.figure(figsize=(8, 6))

        cluster_summary.plot(
            kind="bar"
        )

        plt.title(
            "Average Total Recorded Crimes by Cluster"
        )

        plt.xlabel("Cluster")
        plt.ylabel(
            "Average Total Recorded Crimes"
        )

        plt.xticks(rotation=0)

        plt.tight_layout()

        plt.savefig(
            FIGURE_DIR / "cluster_crime_profile.png",
            dpi=300
        )

        plt.close()

        print("      ✓ cluster_crime_profile.png")

    # =========================================================
    # 9. ELBOW PLOT
    # =========================================================

    elbow_file = (
        TABLE_DIR / "clustering_elbow_results.csv"
    )

    if elbow_file.exists():

        print("\n9. Creating elbow plot")

        elbow = pd.read_csv(
            elbow_file
        )

        plt.figure(figsize=(8, 6))

        plt.plot(
            elbow["k"],
            elbow["inertia"],
            marker="o"
        )

        plt.title(
            "Elbow Method for K-Means Clustering"
        )

        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("Inertia")

        plt.grid(True, alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            FIGURE_DIR / "elbow_method.png",
            dpi=300
        )

        plt.close()

        print("      ✓ elbow_method.png")

    # =========================================================
    # 10. SILHOUETTE SCORE
    # =========================================================

    silhouette_file = (
        TABLE_DIR /
        "clustering_silhouette_results.csv"
    )

    if silhouette_file.exists():

        print("\n10. Creating silhouette score plot")

        silhouette = pd.read_csv(
            silhouette_file
        )

        plt.figure(figsize=(8, 6))

        plt.plot(
            silhouette["k"],
            silhouette["silhouette_score"],
            marker="o"
        )

        plt.title(
            "Silhouette Score by Number of Clusters"
        )

        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("Silhouette Score")

        plt.grid(True, alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            FIGURE_DIR / "silhouette_score.png",
            dpi=300
        )

        plt.close()

        print("      ✓ silhouette_score.png")

    # =========================================================
    # FINAL SUMMARY
    # =========================================================

    print("\nVISUALIZATION SUMMARY")
    print("-" * 40)

    figures = list(
        FIGURE_DIR.glob("*.png")
    )

    print(
        f"Figures generated: {len(figures)}"
    )

    for figure in sorted(figures):
        print(
            f" - {figure.name}"
        )

    print("\n      ✓ Visualization completed")

    return df