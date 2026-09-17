from scripts.data_collection import load_crime_data
from scripts.data_understanding import understand_data
from scripts.data_cleaning import clean_data
from scripts.eda import run_eda
from scripts.statistics import run_statistics
from scripts.pattern_analysis import run_pattern_analysis
from scripts.clustering import run_clustering
from scripts.visualization import run_visualization

def main():

    print("=" * 60)
    print(" MALAYSIAN CRIME ANALYTICS")
    print("=" * 60)

    try:

        # Stage 1
        df = load_crime_data()

        # Stage 2
        df = understand_data(df)

        # Stage 3
        df = clean_data(df)

        # Stage 4
        df = run_eda(df)

        # Stage 5
        df = run_statistics(df)

        # Stage 6
        df = run_pattern_analysis(df)

        # Stage 7
        df = run_clustering(df)

        # Stage 8

        df = run_visualization(df)

        print("\n" + "=" * 60)
        print(" STAGES 1-8 COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception as e:

        print("\n" + "=" * 60)
        print(" ANALYSIS FAILED")
        print("=" * 60)

        print(f"Error: {e}")

        raise


if __name__ == "__main__":
    main()