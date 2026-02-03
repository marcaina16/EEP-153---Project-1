import pandas as pd
from src.panel import build_panel

def test_build_panel_dedupes():
    df = pd.DataFrame({
        "country": ["A", "A"],
        "year": [2000, 2000],
        "ag_export_share": [10.0, 10.0],
    })
    out = build_panel(df)
    assert out.shape[0] == 1
