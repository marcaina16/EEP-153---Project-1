from __future__ import annotations
from typing import Iterable, Tuple, List, Optional
import pandas as pd
from .wb_fetch import fetch_wb_data

SEX={"people":"Total","total":"Total","both":"Total","m":"Male","male":"Male","males":"Male","f":"Female","female":"Female","females":"Female"}
BINS=[(0,14),(15,64),(65,100)]
WB={
  (0,14,"Total"):"SP.POP.0014.TO",(15,64,"Total"):"SP.POP.1564.TO",(65,100,"Total"):"SP.POP.65UP.TO",
  (0,14,"Male"):"SP.POP.0014.MA.IN",(15,64,"Male"):"SP.POP.1564.MA.IN",(65,100,"Male"):"SP.POP.65UP.MA.IN",
  (0,14,"Female"):"SP.POP.0014.FE.IN",(15,64,"Female"):"SP.POP.1564.FE.IN",(65,100,"Female"):"SP.POP.65UP.FE.IN",
}

def _sex(s: str)->str:
  if s in ("Male","Female","Total"): return s
  k=str(s).strip().lower()
  if k in SEX: return SEX[k]
  raise ValueError(f"sex must be Male/Female/Total (or aliases), got {s!r}")

def _bins(age_range: Tuple[int,int])->List[Tuple[int,int]]:
  lo,hi=age_range
  if lo>hi: raise ValueError("age_range must be (low, high) with low<=high")
  out=[(a,b) for (a,b) in BINS if not (hi<a or lo>b)]
  if not out: raise ValueError(f"age_range {age_range} doesn't overlap supported bins {BINS}")
  return out

def population_dataframe(
  places: Iterable[str],
  years: Iterable[int],
  *,
  bins: Optional[List[Tuple[int,int]]]=None,
  sexes: Optional[List[str]]=None,
  cache_path: str="../data/wb_population_cache.csv",
)->pd.DataFrame:
  places=list(places)
  yrs=sorted({int(y) for y in years})
  if not yrs: raise ValueError("years is empty")
  b=bins or BINS
  sx=[_sex(s) for s in (sexes or ["Total","Male","Female"])]

  ind={}
  for (a,c) in b:
    for s in sx:
      ind[WB[(a,c,s)]]=f"pop_{a:02d}_{c:02d}_{s.lower()}"

  # only trust cache if it has EVERYTHING we need
  need={"country","year",*ind.values()}
  if cache_path:
    try:
      cached=pd.read_csv(cache_path)
      if need.issubset(cached.columns):
        return cached.rename(columns={"country":"place"}).set_index(["place","year"]).sort_index()
    except FileNotFoundError:
      pass

  frames=[]
  for p in places:
    df=fetch_wb_data(ind,start_year=yrs[0],end_year=yrs[-1],countries=[p],cache_path=None)
    if "country" not in df.columns: df=df.reset_index()
    if "date" in df.columns and "year" not in df.columns: df=df.rename(columns={"date":"year"})
    if "country" not in df.columns: df["country"]=p
    frames.append(df)

  out=pd.concat(frames,ignore_index=True)
  out=out[out["year"].isin(yrs)].copy()
  out=out.rename(columns={"country":"place"}).set_index(["place","year"]).sort_index()

  if cache_path:
    out.reset_index().rename(columns={"place":"country"}).to_csv(cache_path,index=False)

  return out

def population(year: int, sex: str, age_range: Tuple[int,int], place: str, *, cache_path: str="../data/wb_population_cache.csv")->float:
  s=_sex(sex)
  b=_bins(age_range)
  df=population_dataframe([place],[year],bins=b,sexes=[s],cache_path=cache_path)
  cols=[f"pop_{a:02d}_{c:02d}_{s.lower()}" for (a,c) in b]
  return float(df.loc[(place,year),cols].sum())