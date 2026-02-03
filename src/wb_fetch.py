import os
import pandas as pd

def fetch_wb_data(indicators, start_year, end_year, cache_path=None):
    """
    Fetch World Bank data for given indicators and year range.
    Returns a DataFrame with columns: country, year, <indicator columns>
    """
    if cache_path and os.path.exists(cache_path):
        return pd.read_csv(cache_path)

    import wbdata
    df = wbdata.get_dataframe(indicators, convert_date=False).reset_index()

    # wbdata outputs 'date' for year
    df = df.rename(columns={"date": "year"})
    df["year"] = df["year"].astype(int)
    df = df[(df["year"] >= start_year) & (df["year"] <= end_year)]

    if cache_path:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        df.to_csv(cache_path, index=False)

    return df
