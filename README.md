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
- Produce static publication-ready charts and interactive HTML dashboards for reporting

---

## Project Structure

```
unemployment-analysis/
├── data/
│   ├── raw/                   # Original BPS CSV files — read-only, never modify
│   │   ├── Pengangguran Menurut Golongan Umur, 2021.csv
│   │   ├── Pengangguran Menurut Golongan Umur, 2022.csv
│   │   ├── Pengangguran Menurut Golongan Umur, 2023.csv
│   │   ├── Pengangguran Menurut Golongan Umur, 2024.csv
│   │   └── Pengangguran Menurut Golongan Umur, 2025.csv
│   └── processed/
│       └── unemployment_combined.csv   # Long-format merged dataset (100 rows × 6 columns)
├── notebooks/
│   ├── 01_eda.ipynb           # Data loading, cleaning, sanity checks, EDA
│   └── 02_visualization.ipynb # Interactive Plotly charts and analytical dashboards
├── src/
│   ├── __init__.py
│   ├── loader.py              # Parse and load raw CSVs into DataFrames
│   ├── transform.py           # Cleaning, reshaping, Pydantic validation
│   └── visualize.py           # Reusable charting helpers (Matplotlib, Seaborn, Plotly)
├── tests/
│   ├── conftest.py            # Shared fixtures and pytest configuration
│   ├── test_loader.py
│   ├── test_transform.py
│   ├── test_visualize.py
│   └── fixtures/              # Small sample CSV (year 9999) for test isolation
├── outputs/                   # Generated charts (.png) and interactive figures (.html)
├── main.py                    # Entry point — orchestrates loader → transform → visualize
└── pyproject.toml             # Project metadata and dependencies (uv)
```

---

## Tech Stack

| Layer | Tool / Library | Purpose |
|---|---|---|
| Language | Python ≥ 3.14.3 | Core runtime |
| Package Manager | uv | Dependency management via `pyproject.toml` |
| Data Manipulation | pandas ≥ 2.2.0 | Loading, cleaning, reshaping CSV data |
| Numerical Computing | NumPy ≥ 2.0.0 | Array operations and aggregations |
| Visualization | Matplotlib ≥ 3.9.0, Seaborn ≥ 0.13.0 | Static charts saved to `outputs/` at 150 dpi |
| Dashboard Visualization | Plotly ≥ 5.22.0 | Interactive charts and standalone HTML exports |
| Interactive Analysis | JupyterLab ≥ 4.2.0 | Exploratory data analysis and notebook reporting |
| Data Validation | Pydantic ≥ 2.7.0 | Row-level schema validation with `UnemploymentRecord` |
| Testing | pytest ≥ 8.2.0, pytest-cov ≥ 5.0.0 | Unit tests with ≥75% coverage requirement |
| Code Quality | Ruff ≥ 0.4.0 | Linting (E, W, F, I, UP rules) and formatting |

---

## Pipeline

`main.py` orchestrates the full end-to-end pipeline:

1. **Load** — `src/loader.py`: reads each raw CSV (skipping 5 header rows) and assigns the 7-column schema (`age_group`, `pernah_bekerja_februari`, `pernah_bekerja_agustus`, `tidak_pernah_bekerja_februari`, `tidak_pernah_bekerja_agustus`, `jumlah_februari`, `jumlah_agustus`).
2. **Transform** — `src/transform.py`: removes `Total` rows, casts all numeric columns to `int`, reshapes wide → long format, asserts `pernah_bekerja + tidak_pernah_bekerja == jumlah` for every row, and stacks all years into a single DataFrame.
3. **Validate** — `src/transform.py → validate_records()`: passes every row through the `UnemploymentRecord` Pydantic model; raises `ValueError` on the first failing row.
4. **Save** — writes `data/processed/unemployment_combined.csv` (100 rows × 6 columns: `year`, `period`, `age_group`, `pernah_bekerja`, `tidak_pernah_bekerja`, `jumlah`).
5. **Visualize** — `src/visualize.py`: generates and saves the charts listed below.

---

## Generated Outputs

### Static charts (PNG, 150 dpi) — produced by `main.py`

| File | Description |
|---|---|
| `trend_by_age_group.png` | Unemployment (jumlah) over time, one line per age group |
| `feb_vs_aug.png` | Grouped bar: February vs. August total per year |
| `heatmap.png` | Heatmap: age group × survey period |
| `national_trend.png` | Single-line national total across all 10 survey points |
| `pernah_vs_tidak_trend.png` | Dual-line: Pernah Bekerja vs. Tidak Pernah Bekerja national totals |
| `60plus_volatility.png` | Annotated line for 60+ group, flagging swings > 30% |
| `youth_share.png` | Youth (15–29) unemployment as % of national total |

### Interactive figures (HTML, Plotly) — produced by `notebooks/02_visualization.ipynb`

| File | Description |
|---|---|
| `interactive_trend.html` | Interactive age-group trend chart |
| `national_trend.html` | Interactive national total trend |
| `feb_vs_aug.html` | Interactive Feb vs. Aug comparison |
| `heatmap.html` | Interactive unemployment heatmap |
| `age_group_ranking.html` | Age group ranking by total unemployment |
| `composition_by_age.html` | Pernah/Tidak Pernah composition stacked by age group |
| `pernah_vs_tidak_trend.html` | Interactive dual-line employment-history trend |
| `yoy_change.html` | Year-over-year national % change |
| `yoy_by_age_group.html` | YoY % change grouped by age group |
| `youth_share.html` | Interactive youth share (15–29) line chart |
| `60plus_trend.html` | Interactive 60+ volatility chart |
| `cohort_comparison.html` | Middle-age vs. youth cohort comparison |
| `seasonal_heatmap.html` | Feb–Aug seasonal gap heatmap (% change per age group per year) |

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

### Launch JupyterLab

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
- The **60+ group** may include informal and agricultural workers, making its figures less directly comparable to other age groups across survey periods.
- All figures are **national-level aggregates**; regional or provincial conclusions cannot be drawn.
