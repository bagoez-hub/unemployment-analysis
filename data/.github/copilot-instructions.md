# Copilot Instructions — Unemployment Analysis

## Project Overview

This project analyzes **Indonesian unemployment data by age group (Golongan Umur)** from 2021 to 2025, sourced from BPS (Badan Pusat Statistik / Statistics Indonesia).

Each dataset covers two survey periods per year — **Februari (February)** and **Agustus (August)** — and breaks unemployment figures down across ten age brackets: 15–19, 20–24, 25–29, 30–34, 35–39, 40–44, 45–49, 50–54, 55–59, and 60+.

Unemployment counts are split into three categories:
- **Pernah Bekerja** — previously employed individuals now unemployed
- **Tidak Pernah Bekerja** — individuals who have never been employed
- **Jumlah Pengangguran** — total unemployment (sum of the above two)

All figures are in persons (Orang).

**Goals of this project:**
- Load, clean, and consolidate raw CSV data across all years (2021–2025)
- Identify trends in unemployment by age group over time
- Compare February vs. August survey periods within and across years
- Distinguish patterns between previously-employed and never-employed unemployment
- Produce clear visualizations and summary statistics for reporting

---

## Tech Stack

| Layer | Tool / Library | Purpose |
|---|---|---|
| Language | Python 3.14+ | Core runtime |
| Package Manager | uv | Dependency management via `pyproject.toml` |
| Data Manipulation | pandas | Loading, cleaning, reshaping CSV data |
| Numerical Computing | NumPy | Array operations and aggregations |
| Visualization | Matplotlib, Seaborn | Static charts, trend plots, heatmaps |
| Dashboard Visualization | Plotly | Interactive charts and dashboard figures |
| Interactive Analysis | Jupyter Notebook | Exploratory data analysis (EDA) |
| Data Validation | Pydantic | Schema validation for cleaned/processed data |
| Testing | pytest, pytest-cov | Unit tests and coverage reporting |
| Code Quality | Ruff | Linting and formatting |

---

## Folder Structure

> Legend: ✅ exists — 🔲 planned (to be created)

```
unemployment-analysis/
├── data/                                               ✅
│   ├── .github/                                        ✅
│   │   └── copilot-instructions.md                     ✅  Project rules and AI coding guidelines
│   ├── raw/                                            ✅  Original, unmodified CSV files from BPS — never edit
│   │   ├── Pengangguran Menurut Golongan Umur, 2021.csv
│   │   ├── Pengangguran Menurut Golongan Umur, 2022.csv
│   │   ├── Pengangguran Menurut Golongan Umur, 2023.csv
│   │   ├── Pengangguran Menurut Golongan Umur, 2024.csv
│   │   └── Pengangguran Menurut Golongan Umur, 2025.csv
│   └── processed/                                      🔲  Cleaned and consolidated outputs
│       └── unemployment_combined.csv                   🔲  Long-format merged dataset (all years)
├── notebooks/                                          🔲  Jupyter notebooks for EDA and reporting
│   ├── 01_eda.ipynb                                    🔲  Data loading, cleaning, sanity checks, EDA
│   └── 02_visualization.ipynb                          🔲  Final charts, trend analysis, dashboard figures
├── src/                                                🔲  Importable Python modules (used by main.py & notebooks)
│   ├── __init__.py
│   ├── loader.py                                       🔲  Parse and load raw CSVs into DataFrames
│   ├── transform.py                                    🔲  Cleaning, reshaping, Pydantic validation
│   └── visualize.py                                    🔲  Reusable charting helpers (Matplotlib, Seaborn, Plotly)
├── tests/                                              🔲  Unit tests (pytest)
│   ├── fixtures/                                       🔲  Small sample CSVs for test isolation
│   ├── test_loader.py                                  🔲
│   ├── test_transform.py                               🔲
│   └── test_visualize.py                               🔲
├── outputs/                                            🔲  Generated charts (.png) and interactive figures (.html)
├── .gitignore                                          ✅
├── .python-version                                     ✅  Python version pin (managed by uv)
├── main.py                                             ✅  Entry point — orchestrates loader → transform → outputs
├── pyproject.toml                                      ✅  Project metadata and dependencies (uv)
└── README.md                                           ✅
```

---

## Dataset Summary

| File | Year | Periods | Age Groups | Categories |
|---|---|---|---|---|
| `Pengangguran Menurut Golongan Umur, 2021.csv` | 2021 | Feb, Aug | 15–19 → 60+ | Pernah Bekerja, Tidak Pernah Bekerja, Jumlah |
| `Pengangguran Menurut Golongan Umur, 2022.csv` | 2022 | Feb, Aug | 15–19 → 60+ | Pernah Bekerja, Tidak Pernah Bekerja, Jumlah |
| `Pengangguran Menurut Golongan Umur, 2023.csv` | 2023 | Feb, Aug | 15–19 → 60+ | Pernah Bekerja, Tidak Pernah Bekerja, Jumlah |
| `Pengangguran Menurut Golongan Umur, 2024.csv` | 2024 | Feb, Aug | 15–19 → 60+ | Pernah Bekerja, Tidak Pernah Bekerja, Jumlah |
| `Pengangguran Menurut Golongan Umur, 2025.csv` | 2025 | Feb, Aug | 15–19 → 60+ | Pernah Bekerja, Tidak Pernah Bekerja, Jumlah |

> All raw CSVs share the same multi-header layout (rows 1–4 are header rows) and must be parsed with `header=None` and manually labeled columns before use.

---

## EDA Checkpoints

Use these checkpoints sequentially during exploratory data analysis to ensure data quality and completeness before moving to analysis.

### 1. Data Loading & Structure
- [ ] All 5 CSV files load without errors
- [ ] Multi-row headers are correctly skipped; columns are manually renamed
- [ ] Age group labels (`15-19`, `20-24`, ..., `60+`) are consistent across all years
- [ ] `Total` rows are identified and separated from age-group rows

### 2. Data Types & Cleaning
- [ ] All count columns are cast to `int` or `int64` (no string remnants)
- [ ] No unexpected null/NaN values in any figure column
- [ ] Age group column is treated as a categorical/ordered variable
- [ ] Year and period (Februari / Agustus) columns exist after reshaping

### 3. Consolidation
- [ ] All 5 years are stacked into a single long-format DataFrame (`unemployment_combined.csv`)
- [ ] Columns: `year`, `period`, `age_group`, `pernah_bekerja`, `tidak_pernah_bekerja`, `jumlah`
- [ ] Verify row count: 5 years × 2 periods × 10 age groups = **100 rows** (excluding totals)
- [ ] Total rows stored separately for cross-validation

### 4. Sanity Checks
- [ ] `pernah_bekerja + tidak_pernah_bekerja == jumlah` for every row
- [ ] Annual totals match BPS-published national figures (spot check)
- [ ] No duplicate rows (same year + period + age group)
- [ ] February and August figures both exist for every year

### 5. Distribution & Outliers
- [ ] Descriptive statistics (`mean`, `std`, `min`, `max`) per age group
- [ ] Identify the age group with consistently the highest unemployment across all years
- [ ] Flag any year-over-year change greater than 30% as a point of interest
- [ ] Check whether 2021 figures are anomalously high (COVID-19 effect)

---

## Possible Analytical Questions

1. **Which age group has the highest total unemployment across all years?**
   — Is the 20–24 cohort persistently the most affected, as raw totals suggest?

2. **How has total unemployment trended from 2021 to 2025?**
   — Is there a consistent decline post-pandemic, or did it plateau?

3. **What is the February vs. August gap, and is it consistent year to year?**
   — Does one survey period systematically show higher unemployment?

4. **Which age group shows the steepest year-on-year improvement (reduction)?**
   — Are younger cohorts recovering faster than older ones?

5. **How does the ratio of Pernah Bekerja vs. Tidak Pernah Bekerja shift by age group?**
   — Younger groups are expected to skew toward "never worked"; does this hold?

6. **Did the 60+ group behave differently from other groups during 2021–2022 (pandemic recovery)?**
   — Older workers may have exited the labor force rather than registering as unemployed.

7. **What proportion of total unemployment is accounted for by youth (15–29)?**
   — How does this youth share change between 2021 and 2025?

8. **Is there a seasonal pattern in any specific age group between February and August?**
   — E.g., school/university graduation cycles inflating August figures for 20–24.

9. **Which years saw the sharpest single-period drops in total unemployment?**
   — Identifying policy-relevant turning points.

10. **How does middle-age unemployment (35–54) compare in magnitude and trend to youth unemployment (15–29)?**

---

## Possible Insights

1. **Youth unemployment dominance** — The 20–24 age group consistently accounts for the largest share of total unemployment across all years and periods, pointing to a structural gap between education completion and labor market absorption.

2. **Post-pandemic recovery trajectory** — Total unemployment peaked around 2021 (Agustus: ~9.1 million) and shows a general downward trend toward 2025 (~7.3–7.5 million), suggesting labor market recovery, though the pace varies by age.

3. **Never-employed concentrated in youth** — The `Tidak Pernah Bekerja` category is disproportionately large in the 15–19 and 20–24 brackets, reflecting first-time job seekers — a signal for early-career policy interventions.

4. **Seasonal fluctuation varies by cohort** — August figures for certain age groups (notably 20–24 and 60+) are notably different from February, likely reflecting graduation-driven labor supply surges and informal/seasonal work patterns in older cohorts.

5. **60+ group volatility** — The 60+ age group shows large swings between periods (e.g., 195K Feb 2021 vs. 419K Aug 2021), suggesting this cohort's unemployment count is sensitive to how informal and agricultural labor is captured in each survey wave.

6. **Middle-age stabilization** — Cohorts aged 35–54 show relatively stable and low unemployment compared to youth, indicating stronger labor market attachment once employed, but also slower absolute recovery when displaced.

7. **Declining previously-employed unemployment** — The `Pernah Bekerja` totals decline more steeply than `Tidak Pernah Bekerja` across most years, implying re-employment of displaced workers is progressing faster than first-time labor market entry.

8. **2025 partial stabilization** — 2025 figures hover around 7.3–7.5 million total unemployed, close to 2024 levels, which may indicate the economy is approaching a structural unemployment floor rather than continuing the post-2021 recovery trend.

---

## Rules & Limitations

### Code Style
- Follow **PEP 8** strictly. All code must pass `ruff check` and `ruff format` with zero errors before committing.
- Use **type hints** on all function signatures in `src/`. No untyped public functions.
- Keep functions **single-purpose** and small (< 40 lines). If a function is growing beyond that, split it.
- No logic inside `main.py` beyond orchestrating calls to `src/` modules.
- Avoid hardcoding file paths — use `pathlib.Path` and define root paths as constants in a config module or at the top of each script.
- Never modify files inside `data/raw/`. Raw data is read-only; all transformations produce outputs to `data/processed/` or `outputs/`.

### Data Handling
- Always validate the cleaned DataFrame shape and column names using **Pydantic** models before passing data to analysis or visualization functions.
- The canonical long-format schema for the processed dataset is: `year (int)`, `period (str: 'Februari'|'Agustus')`, `age_group (str)`, `pernah_bekerja (int)`, `tidak_pernah_bekerja (int)`, `jumlah (int)`.
- Assert `pernah_bekerja + tidak_pernah_bekerja == jumlah` for every row after loading. Raise a `ValueError` if this invariant is violated.
- `Total` rows must be separated from age-group rows and never mixed into group-level analysis.
- Do not impute or fill missing values silently — raise an explicit error if unexpected nulls are detected.

### Visualization
- **Matplotlib / Seaborn** — use for static, publication-ready charts saved to `outputs/`.
- **Plotly** — use for interactive figures inside Jupyter notebooks or exported as standalone HTML to `outputs/`.
- Do not mix Plotly and Matplotlib in the same chart. Pick one per figure.
- All charts must include: a descriptive **title**, labeled **axes with units**, a **legend** if multiple series are shown, and a **source note** ("Source: BPS, [year]").
- Color palettes must be colorblind-safe. Prefer `seaborn`'s `colorblind` palette for Matplotlib and Plotly's `safe` or `Plotly` discrete sequences.
- Never display raw counts without context — always label axes as "Jumlah Pengangguran (Orang)" or equivalent.
- Save all output figures at a minimum resolution of **150 dpi** (Matplotlib) or as **vector-compatible HTML** (Plotly).

### Testing
- All functions in `src/` must have corresponding unit tests under `tests/`.
- Use **pytest** for all tests. Test files follow the naming convention `test_<module>.py`.
- Minimum acceptable coverage is **75%** — enforced via `pytest-cov`. Run with: `pytest --cov=src --cov-report=term-missing`.
- Tests must not read from `data/raw/` — use small inline fixtures or files in a `tests/fixtures/` directory.
- Do not test Jupyter notebooks — only test importable `src/` modules.

### Limitations
- Data covers only **2021–2025**; do not extrapolate trends beyond 2025 without explicit caveats.
- The BPS dataset does not include gender, education level, or province — analyses are limited to **age group and employment history** dimensions.
- February and August are **point-in-time surveys**, not continuous tracking — intra-year monthly trends cannot be inferred.
- The 60+ group may include both retirees and informal workers, making its numbers less comparable to other age groups. Flag this in any 60+ analysis.
- All figures are **national-level aggregates**; regional or provincial conclusions cannot be drawn from this dataset.

---

### Jupyter Notebook Rules (Kaggle-Ready)

#### Structure & Cell Order
- Every notebook must be **fully runnable top-to-bottom** with **Kernel → Restart & Run All** producing zero errors. Never submit a notebook that requires manual cell re-ordering.
- Follow this mandatory section order:
  1. **Title & Description** — Markdown cell: project title, objective, data source, author.
  2. **Imports** — single cell, all `import` statements at the top. No imports buried mid-notebook.
  3. **Configuration / Constants** — paths, color palettes, display settings (`pd.set_option`, `plt.rcParams`).
  4. **Data Loading** — load and display raw shape + `.head()`.
  5. **Data Cleaning & Validation** — transformations, Pydantic validation, sanity checks.
  6. **EDA** — distributions, aggregations, descriptive statistics.
  7. **Visualization** — all charts in logical sequence.
  8. **Summary / Conclusions** — Markdown cell summarizing key findings.

#### Kaggle Compatibility
- Use **relative paths** for data files. On Kaggle, datasets are mounted at `/kaggle/input/`. Use `pathlib.Path` with a fallback:
  ```python
  from pathlib import Path
  DATA_DIR = Path("/kaggle/input/unemployment-indonesia") if Path("/kaggle").exists() else Path("data/raw")
  ```
- Do **not** use `uv`, `pyproject.toml`, or any local package installs inside the notebook. All dependencies must be available in the Kaggle base Python environment or installed via `!pip install <package>` at the top of the notebook.
- If `!pip install` is needed (e.g., Plotly version pinning), place it in the **first code cell**, isolated from imports.
- Do not use `sys.path` manipulation or relative imports from `src/`. Copy required helper logic inline or re-implement it in the notebook for Kaggle portability.

#### Cell Hygiene
- Each code cell must have a **single, clear responsibility**. No cell should both load data and clean it simultaneously.
- Every major section must be preceded by a **Markdown header cell** (using `##` or `###`) that names the section.
- After every data transformation step, display the resulting DataFrame shape and a `.head()` or `.sample(5)` so the reader can verify state.
- Keep cell output visible — do not suppress all output. At minimum, show shape confirmations and final chart outputs.
- Remove all debug `print` statements and scratch cells before finalizing the notebook.

#### Visualization in Notebooks
- Prefer **Plotly** for Kaggle notebooks — interactive charts render natively in the Kaggle viewer.
- Always call `fig.show()` for Plotly figures; do not rely on implicit display.
- For Matplotlib, always end a cell with `plt.tight_layout(); plt.show()` — never leave figures to render implicitly.
- Add `fig.update_layout(title=..., xaxis_title=..., yaxis_title=...)` to every Plotly figure. No untitled charts.

#### Documentation & Reproducibility
- The first Markdown cell must include: **dataset name**, **source URL or BPS reference**, **date of data**, and **notebook purpose**.
- Use Markdown cells to explain *why* each analysis step is performed, not just *what* is being done.
- Pin random seeds where relevant: `import random; random.seed(42)` / `np.random.seed(42)`.
- The notebook must produce **identical outputs** on every clean run — no randomness, no network calls, no side effects dependent on external state.
