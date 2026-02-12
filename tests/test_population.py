import math
import pandas as pd
import pytest
from src.population import population, population_dataframe
def test_population_world_positive():
    v = population(2000, "Total", (0,14), "WLD")
    assert v > 0 and math.isfinite(v)
def test_population_aliases_match():
    a = population(2000, "people", (15,64), "WLD")
    b = population(2000, "Total", (15,64), "WLD")
    assert abs(a-b)/b < 1e-12
def test_population_male_female_positive():
    m = population(2000, "Male", (65,100), "WLD")
    f = population(2000, "Female", (65,100), "WLD")
    assert m > 0 and f > 0
def test_population_dataframe_shape_and_cols():
    df = population_dataframe(["WLD","USA"], [2000,2001])
    assert isinstance(df, pd.DataFrame)
    assert ("WLD", 2000) in df.index
    assert "pop_00_14_male" in df.columns
    assert "pop_15_64_female" in df.columns
def test_bad_sex_raises():
    with pytest.raises(ValueError):
        population(2000, "Robot", (0,14), "WLD")
def test_bad_age_range_raises():
    with pytest.raises(ValueError):
        population(2000, "Total", (20,10), "WLD")
