import pandas as pd

URL_DATA = "https://storage.data.gov.my/publicsafety/crime_district.parquet"


def load_crime_data():
    print("[1/8] Data Collection")

    try:
        df = pd.read_parquet(URL_DATA)

        print("      ✓ Crime dataset loaded")
        print(f"      Rows    : {len(df):,}")
        print(f"      Columns : {len(df.columns)}")

        return df

    except Exception as e:
        print("      ✗ Data collection failed")
        raise RuntimeError(f"Unable to load crime dataset: {e}")