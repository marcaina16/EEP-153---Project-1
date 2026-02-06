# EEP 153 Project 1 — Agricultural Export Dependence & Mortality (WBData)

## Project goal
We build a country-year dataset (2000–2022) using World Bank data to explore whether **agricultural export dependence** and **agricultural production** relate to **adult mortality** over time.
We include **countries + territories** and exclude WB “Aggregates” (regions/income groups).

## Repo structure
- `src/` — code for fetching WBData + building the analysis panel
- `notebooks/` — demo notebook that runs the pipeline end-to-end
- `tests/` — unit tests (run with pytest)

## How to run (for code review)
From the repo root:

1) Install packages (if needed):
```bash
pip install --user wbdata pandas pytest
