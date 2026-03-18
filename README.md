# Unemployment Analysis — Indonesia by Age Group (2021–2025)

## Overview

This project analyzes **Indonesian unemployment data by age group (Golongan Umur)** from 2021 to 2025, using datasets published by **BPS — Badan Pusat Statistik (Statistics Indonesia)**.

Each dataset covers **two survey periods per year** — **Februari (February)** and **Agustus (August)** — and breaks unemployment figures down across **ten age brackets**: 15–19, 20–24, 25–29, 30–34, 35–39, 40–44, 45–49, 50–54, 55–59, and 60+.

Unemployment counts are split into three categories:

| Category | Description |
|---|---|
| **Pernah Bekerja** | Previously employed individuals now unemployed |
| **Tidak Pernah Bekerja** | Individuals who have never been employed |
| **Jumlah Pengangguran** | Total unemployment (sum of the above two) |

All figures are in persons (Orang) and represent **national-level aggregates**.

---

## Purpose

- Load, clean, and consolidate raw CSV data across all years (2021–2025) into a single long-format dataset
- Identify trends in unemployment by age group over time
- Compare February vs. August survey periods within and across years
- Distinguish patterns between previously-employed and never-employed unemployment
- Produce clear visualizations and summary statistics for reporting

---

## Project Structure

```
unemployment-analysis/
├── data/
│   ├── raw/                   # Original BPS CSV files — read-only, never modify
│   └── processed/             # Cleaned and consolidated outputs
├── notebooks/
│   ├── 01_eda.ipynb           # Data loading, cleaning, sanity checks, EDA
│   └── 02_visualization.ipynb # Final charts, trend analysis, dashboard figures
├── src/
│   ├── loader.py              # Parse and load raw CSVs into DataFrames
│   ├── transform.py           # Cleaning, reshaping, Pydantic validation
│   └── visualize.py           # Reusable charting helpers (Matplotlib, Seaborn, Plotly)
├── tests/                     # Unit tests (pytest)
│   └── fixtures/              # Small sample CSVs for test isolation
├── outputs/                   # Generated charts (.png) and interactive figures (.html)
├── main.py                    # Entry point — orchestrates the full pipeline
└── pyproject.toml             # Project metadata and dependencies (uv)
```

---

## Tech Stack

| Layer | Tool / Library | Purpose |
|---|---|---|
| Language | Python 3.14+ | Core runtime |
| Package Manager | uv | Dependency management |
| Data Manipulation | pandas | Loading, cleaning, reshaping CSV data |
| Numerical Computing | NumPy | Array operations and aggregations |
| Visualization | Matplotlib, Seaborn | Static charts saved to `outputs/` |
| Dashboard Visualization | Plotly | Interactive charts and HTML exports |
| Interactive Analysis | Jupyter Lab | Exploratory data analysis (EDA) |
| Data Validation | Pydantic | Schema validation for cleaned/processed data |
| Testing | pytest, pytest-cov | Unit tests with ≥75% coverage requirement |
| Code Quality | Ruff | Linting and formatting enforcement |

---

## Getting Started

### Install dependencies

```bash
uv sync --group dev
```

### Run the analysis pipeline

```bash
uv run python main.py
```

### Run tests

```bash
uv run pytest --cov=src --cov-report=term-missing
```

### Lint and format

```bash
uv run ruff check .
uv run ruff format .
```

### Launch Jupyter Lab

```bash
uv run jupyter lab
```

---

## Data Source

**BPS — Badan Pusat Statistik (Statistics Indonesia)**  
Dataset: *Pengangguran Menurut Golongan Umur* (Unemployment by Age Group)  
Coverage: 2021 Februari – 2025 Agustus  

> **Note:** Raw data files in `data/raw/` are read-only. All outputs are written to `data/processed/` or `outputs/`.

---

## Limitations

- Data covers only **2021–2025** — trends cannot be extrapolated beyond this range without caveats.
- The dataset does not include gender, education level, or province — analyses are limited to **age group and employment history** dimensions.
- February and August are **point-in-time surveys**, not continuous tracking — intra-year monthly trends cannot be inferred.
- All figures are **national-level aggregates**; regional or provincial conclusions cannot be drawn.
