# EEP 153 Project 1 — World Bank Panel + Export Dependence

## What this repo does
This repo pulls World Bank indicator data (2000–2022), builds a country-year panel, and creates an `export_dependent` label based on agricultural export share.

## Repo structure
- `src/` — core code (WB data pull + panel construction)
- `notebooks/` — demo notebook showing the workflow end-to-end
- `tests/` — unit tests (run with pytest)

## How to run (recommended)
1) Install dependencies (if needed):
```bash
pip install --user wbdata pandas pytest
