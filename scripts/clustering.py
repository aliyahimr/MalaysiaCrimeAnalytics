import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


OUTPUT_DIR = Path("outputs/tables")


def run_clustering(df):

    print("\n[7/8] Clustering Analysis")
    print("=" * 50)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = df.copy()

    # ---------------------------------------------------------
    # 1. PREPARE YEAR
    # ---------------------------------------------------------

    print("\n1. Preparing dataset")

    df["year"] = df["date"].dt.year

    print("      ✓ Year extracted")

    # ---------------------------------------------------------
    # 2. CREATE DISTRICT-LEVEL FEATURES
    # ---------------------------------------------------------

    print("\n2. Creating district-level features")

    district_features = (
        df.groupby("district")
        .agg(
            total_crimes=("crimes", "sum"),
            mean_crimes=("crimes", "mean"),
            median_crimes=("crimes", "median"),
            std_crimes=("crimes", "std"),
            min_crimes=("crimes", "min"),
            max_crimes=("crimes", "max"),
            active_categories=("category", "nunique"),
            active_types=("type", "nunique"),
            years_recorded=("year", "nunique")
        )
        .reset_index()
    )

    # Replace missing standard deviation
    # with 0 for districts with only one observation.
    district_features["std_crimes"] = (
        district_features["std_crimes"]
        .fillna(0)
    )

    print(
        f"      Districts available: "
        f"{len(district_features):,}"
    )

    print("\nDISTRICT FEATURES")
    print(
        district_features
        .head(10)
        .to_string(index=False)
    )

    district_features.to_csv(
        OUTPUT_DIR / "district_clustering_features.csv",
        index=False
    )

    # ---------------------------------------------------------
    # 3. SELECT FEATURES
    # ---------------------------------------------------------

    print("\n3. Selecting clustering features")

    feature_columns = [
        "total_crimes",
        "mean_crimes",
        "median_crimes",
        "std_crimes",
        "min_crimes",
        "max_crimes",
        "active_categories",
        "active_types",
        "years_recorded"
    ]

    X = district_features[feature_columns].copy()

    print("      Features selected:")

    for feature in feature_columns:
        print(f"      - {feature}")

    # ---------------------------------------------------------
    # 4. HANDLE INVALID VALUES
    # ---------------------------------------------------------

    print("\n4. Checking feature values")

    if X.isnull().sum().sum() > 0:
        print("      ⚠ Missing feature values detected")

        X = X.replace(
            [np.inf, -np.inf],
            np.nan
        )

        X = X.fillna(0)

    else:
        print("      ✓ No missing feature values")

    if np.isinf(X.to_numpy()).any():
        raise ValueError(
            "Infinite values detected in clustering features."
        )

    print("      ✓ Feature values validated")

    # ---------------------------------------------------------
    # 5. STANDARDISE FEATURES
    # ---------------------------------------------------------

    print("\n5. Standardising features")

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    print("      ✓ Features standardised")

    # ---------------------------------------------------------
    # 6. ELBOW METHOD
    # ---------------------------------------------------------

    print("\n6. Running Elbow Method")

    max_k = min(10, len(district_features) - 1)

    if max_k < 2:
        raise ValueError(
            "Not enough districts available for clustering."
        )

    inertia_values = []

    for k in range(2, max_k + 1):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(X_scaled)

        inertia_values.append(
            model.inertia_
        )

        print(
            f"      k={k}: "
            f"inertia={model.inertia_:,.2f}"
        )

    elbow_results = pd.DataFrame({
        "k": range(2, max_k + 1),
        "inertia": inertia_values
    })

    elbow_results.to_csv(
        OUTPUT_DIR / "clustering_elbow_results.csv",
        index=False
    )

    print(
        "      ✓ Elbow results saved"
    )

    # ---------------------------------------------------------
    # 7. SILHOUETTE SCORE
    # ---------------------------------------------------------

    print("\n7. Calculating Silhouette Scores")

    silhouette_results = []

    for k in range(2, max_k + 1):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(X_scaled)

        score = silhouette_score(
            X_scaled,
            labels
        )

        silhouette_results.append({
            "k": k,
            "silhouette_score": score
        })

        print(
            f"      k={k}: "
            f"silhouette={score:.4f}"
        )

    silhouette_df = pd.DataFrame(
        silhouette_results
    )

    silhouette_df.to_csv(
        OUTPUT_DIR / "clustering_silhouette_results.csv",
        index=False
    )

    # ---------------------------------------------------------
    # 8. SELECT K
    # ---------------------------------------------------------

    best_row = silhouette_df.loc[
        silhouette_df["silhouette_score"].idxmax()
    ]

    best_k = int(best_row["k"])

    print("\n8. Selecting number of clusters")

    print(
        f"      Selected k: {best_k}"
    )

    print(
        f"      Silhouette score: "
        f"{best_row['silhouette_score']:.4f}"
    )

    # ---------------------------------------------------------
    # 9. FINAL K-MEANS
    # ---------------------------------------------------------

    print("\n9. Running final K-Means model")

    final_model = KMeans(
        n_clusters=best_k,
        random_state=42,
        n_init=10
    )

    district_features["cluster"] = (
        final_model.fit_predict(X_scaled)
    )

    print("      ✓ K-Means clustering completed")

    # ---------------------------------------------------------
    # 10. SAVE CLUSTER ASSIGNMENTS
    # ---------------------------------------------------------

    print("\n10. Saving cluster assignments")

    district_features = district_features.sort_values(
        ["cluster", "total_crimes"],
        ascending=[True, False]
    )

    district_features.to_csv(
        OUTPUT_DIR / "district_clusters.csv",
        index=False
    )

    print(
        "      ✓ Saved: "
        "district_clusters.csv"
    )

    # ---------------------------------------------------------
    # 11. CLUSTER SUMMARY
    # ---------------------------------------------------------

    print("\n11. Cluster summary")

    cluster_summary = (
        district_features
        .groupby("cluster")
        .agg(
            districts=("district", "count"),
            total_crimes_mean=("total_crimes", "mean"),
            mean_crimes_mean=("mean_crimes", "mean"),
            median_crimes_mean=("median_crimes", "mean"),
            std_crimes_mean=("std_crimes", "mean"),
            active_categories_mean=(
                "active_categories",
                "mean"
            ),
            active_types_mean=(
                "active_types",
                "mean"
            )
        )
        .reset_index()
    )

    print(
        cluster_summary.to_string(index=False)
    )

    cluster_summary.to_csv(
        OUTPUT_DIR / "cluster_summary.csv",
        index=False
    )

    # ---------------------------------------------------------
    # 12. FINAL SUMMARY
    # ---------------------------------------------------------

    print("\nCLUSTERING SUMMARY")
    print("-" * 40)

    print(
        f"Districts clustered : "
        f"{len(district_features):,}"
    )

    print(
        f"Number of clusters  : "
        f"{best_k}"
    )

    print(
        f"Best silhouette     : "
        f"{best_row['silhouette_score']:.4f}"
    )

    print("\n      ✓ Clustering completed")

    return df