import os
import time
import pandas as pd

def fetch_wb_data(indicators, start_year, end_year, cache_path=None, countries=None, max_retries=3):
    """
    Fetch World Bank data using wbdata.

    indicators: dict like {"CODE":"clean_name", ...}
    countries: list like ["USA","BRA"] or "USA" or None for ALL countries
    """
    if cache_path and os.path.exists(cache_path):
        return pd.read_csv(cache_path)

    import wbdata

    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            kwargs = {
                "date": (str(start_year), str(end_year))  # strings required in your wbdata
            }
            # Only include country if it is NOT None
            if countries is not None:
                kwargs["country"] = countries

            df = wbdata.get_dataframe(indicators, **kwargs).reset_index()
            break

        except Exception as e:
            last_err = e
            time.sleep(1.5 * attempt)
    else:
        raise last_err

    # Convert date -> year
    if "date" not in df.columns:
        raise ValueError(f"Expected a 'date' column, got: {df.columns.tolist()}")

    df["year"] = df["date"].astype(str).str[:4].astype(int)
    df = df.drop(columns=["date"])

    # Rename columns if wbdata returned codes instead of clean names
    for code, clean in indicators.items():
        if code in df.columns and clean not in df.columns:
            df = df.rename(columns={code: clean})

    if cache_path:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        df.to_csv(cache_path, index=False)

    return df
