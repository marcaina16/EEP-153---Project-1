from functools import lru_cache
from typing import Iterable, Tuple, List, Optional
import pandas as pd
import wbdata
from .wb_fetch import fetch_wb_data
SEX={"people":"Total","total":"Total","both":"Total","male":"Male","males":"Male","m":"Male","female":"Female","females":"Female","f":"Female"}
BINS=[(0,14),(15,64),(65,100)]
WDI={(0,14):{"Total":"SP.POP.0014.TO","Male":"SP.POP.0014.MA.IN","Female":"SP.POP.0014.FE.IN"},
  (15,64):{"Total":"SP.POP.1564.TO","Male":"SP.POP.1564.MA.IN","Female":"SP.POP.1564.FE.IN"},
  (65,100):{"Total":"SP.POP.65UP.TO","Male":"SP.POP.65UP.MA.IN","Female":"SP.POP.65UP.FE.IN"},}
def _sex(s: str)->str:
  if s in ("Male","Female","Total"): return s
  k=str(s).strip().lower()
  if k in SEX: return SEX[k]
  raise ValueError(f"sex must be Male/Female/Total (or alias), got {s!r}")
@lru_cache(maxsize=256)
def _code(place: str)->str:
  p=str(place).strip()
  if len(p) in (3,4) and p.isupper(): return p
  try:
    c=wbdata.get_country(p)
    if isinstance(c,dict) and "id" in c: return c["id"]
  except Exception:
    pass
  raise ValueError(f"place={place!r} not recognized; use WB code like 'WLD' or 'USA'")
def population(year: int, sex: str, age_range: Tuple[int,int], place: str, *, cache_path: str="../data/wb_population_cache.csv")->float:
  s=_sex(sex); lo,hi=age_range
  if lo>hi: raise ValueError("age_range must be (low, high) with low<=high")
  bins=[(a,b) for (a,b) in BINS if not (hi<a or lo>b)]
  if not bins: raise ValueError(f"age_range {age_range} doesn't overlap supported bins {BINS}")
  ind={}
  for (a,b) in bins: ind[WDI[(a,b)][s]]=f"pop_{a:02d}_{b:02d}_{s.lower()}"
  df=fetch_wb_data(ind,start_year=year,end_year=year,countries=[_code(place)],cache_path=cache_path)
  if "country" not in df.columns: df=df.reset_index()
  if "year" not in df.columns and "date" in df.columns: df=df.rename(columns={"date":"year"})
  if "country" not in df.columns: df["country"]=place
  return float(df.loc[df["year"]==year, list(ind.values())].sum(axis=1).iloc[0])
def population_dataframe(places, years, *, bins=None, sexes=None, cache_path="../data/wb_population_cache.csv"):
  yrs=sorted({int(y) for y in years})
  if not yrs: raise ValueError("years is empty")
  b=bins or BINS
  sx=sexes or ["Male","Female","Total"]
  pcs=[_code(p) for p in places]
  ind={}
  for (a,c) in b:
    for s0 in sx:
      s=_sex(s0)
      ind[WDI[(a,c)][s]]=f"pop_{a:02d}_{c:02d}_{s.lower()}"
  frames=[]
  for code in pcs:
    cp=cache_path
    if cp and cp.endswith(".csv"): cp=cp[:-4]+f"_{code}.csv"
    df=fetch_wb_data(ind,start_year=yrs[0],end_year=yrs[-1],countries=[code],cache_path=cp)
    if "country" not in df.columns: df=df.reset_index()
    if "year" not in df.columns and "date" in df.columns: df=df.rename(columns={"date":"year"})
    if "country" not in df.columns: df["country"]=code
    frames.append(df)
  out=pd.concat(frames,ignore_index=True)
  out=out.rename(columns={"country":"place"})
  return out.set_index(["place","year"]).sort_index()