import pandas as pd
def classify_export_dependent(
    df,
    export_col="ag_export_share",
    base_years=(2000, 2010),
    top_quantile=0.75):
    y0, y1 = base_years
    base = df[(df["year"] >= y0) & (df["year"] <= y1)]
    avg = base.groupby("country")[export_col].mean()
    threshold = avg.quantile(top_quantile)
    def label(country):
        val = avg.get(country)
        return bool(val >= threshold) if pd.notna(val) else False
    return df["country"].map(label)
def build_panel(df):
    df = df.drop_duplicates(subset=["country", "year"]).copy()
    if "ag_export_share" not in df.columns:
        raise ValueError("Expected column 'ag_export_share' in df")
    df["export_dependent"] = classify_export_dependent(df)
    return df
