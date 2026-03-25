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
├── .github/                                            ✅
│   └── copilot-instructions.md                         ✅  Project rules and AI coding guidelines
├── data/                                               ✅
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
├── .gitconfig                                          ✅
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

> Each question is paired with the recommended visualization type that answers it.

1. **Which age group has the highest total unemployment across all years?**
   — Is the 20–24 cohort persistently the most affected, as raw totals suggest?
   *→ Grouped bar chart ranking age groups by total `jumlah` per year.*

2. **How has national total unemployment trended from 2021 to 2025 across all 10 survey points?**
   — Is there a consistent post-pandemic decline, or did it plateau after 2024?
   *→ Single-line chart aggregating all age groups into a national total per survey period.*

3. **What is the February vs. August gap per year, and is it consistent?**
   — Does one survey period systematically show higher unemployment, and why?
   *→ Grouped bar chart (Feb vs. Aug per year) to visualise direction and magnitude of gap.*

4. **Which age group shows the steepest year-on-year improvement (reduction)?**
   — Are younger cohorts recovering faster than older ones?
   *→ YoY % change grouped bar chart, split by survey period.*

5. **How does the Pernah Bekerja vs. Tidak Pernah Bekerja composition vary by age group?**
   — Younger groups are expected to skew toward "never worked"; does this hold across all years?
   *→ Stacked bar chart averaged over all periods, one bar per age group.*

6. **How have national Pernah Bekerja and Tidak Pernah Bekerja totals diverged over time?**
   — Is re-employment of displaced workers outpacing first-time labor market entry?
   *→ Dual-line chart tracking both national totals across all 10 survey periods.*

7. **Did the 60+ group behave differently from other groups during 2021–2022?**
   — The 60+ group shows 100%+ swings between Feb and Aug in 2021–2022; what drives this volatility?
   *→ Isolated annotated line chart for the 60+ cohort, with large inter-period changes flagged.*

8. **What proportion of total unemployment is accounted for by youth (15–29)?**
   — Is the youth share declining as the labor market recovers, or structurally fixed?
   *→ Line chart of youth (15–29) `jumlah` as a percentage of national total per survey period.*

9. **Is there a seasonal pattern in any specific age group between February and August?**
   — E.g., graduation cycles inflating August figures for 20–24; informal work suppressing 60+ in February.
   *→ Computed as `(Aug − Feb) / Feb × 100` per age group per year; visualised as a heatmap.*

10. **Which years saw the sharpest single-period drops in total unemployment?**
    — Identifying policy-relevant turning points in the post-pandemic recovery.
    *→ YoY % change chart (see Q4); flag bars exceeding −10% or +10% as significant.*

11. **How does middle-age unemployment (35–54) compare in magnitude and trend to youth (15–29)?**
    — Middle-age cohorts are expected to be more stable; does the data confirm this across all years?
    *→ Unemployment trend by age group line chart with cohorts visually grouped.*

---

## Possible Insights

1. **Youth unemployment dominance** — The 20–24 age group consistently accounts for ~30–35% of national total unemployment across all years and periods, pointing to a structural gap between education completion and labor market absorption. This share remains largely stable even as total figures decline.

2. **Post-pandemic recovery trajectory** — National total unemployment peaked around Aug 2021 (~9.1 million) and declined to ~7.3–7.5 million by 2024–2025, across 10 consecutive survey points. The decline is not linear — 2022 saw the steepest drop, with 2024–2025 showing signs of plateauing.

3. **Never-employed concentrated in youth** — The `Tidak Pernah Bekerja` share of total unemployment in Feb 2025 is ~80% for 15–19, ~60% for 20–24, and drops below 25% for groups 35 and older. This gradient confirms first-time job seekers are the structural core of youth unemployment.

4. **Pernah Bekerja declining faster than Tidak Pernah Bekerja** — National `pernah_bekerja` totals fell from ~5.5M (Feb 2021) to ~3.6M (Feb 2025), a drop of ~34%. National `tidak_pernah_bekerja` totals remained in the 3.2–3.4M range across the same span — essentially flat. Re-employment of displaced workers is accelerating; first-time labor market entry is not.

5. **Seasonal fluctuation varies sharply by cohort** — The 15–19 group shows large August spikes driven by school-leavers entering the labor market mid-year (e.g., Aug 2022: 1,856K vs. Feb 2022: 1,134K, a +64% gap). The 60+ group shows even larger swings (Aug 2021: 419K vs. Feb 2021: 196K, +114%), suggesting sensitivity to how informal and agricultural labor is counted across survey waves.

6. **60+ group volatility is anomalous** — The 60+ cohort's February–August swing exceeds 100% in 2021 and 2022, far beyond any other age group. This is not characteristic of a retirement-age demographic and should be flagged as a data-capture artefact tied to seasonal informal employment rather than genuine unemployment cycles.

7. **Middle-age stabilization** — Cohorts aged 35–54 combined represent a small and relatively stable share of total unemployment (roughly 15–20%). Their absolute values show mild decline from 2021 to 2025, but far slower relative recovery than youth cohorts — suggesting displaced mid-career workers face longer re-employment durations.

8. **2025 structural floor hypothesis** — Total unemployment in 2025 (Feb: ~7.3M, Aug: ~7.5M) is nearly identical to 2024 levels. YoY change magnitude is approaching 0%, consistent with the economy reaching a structural unemployment floor rather than continuing the post-pandemic recovery trend. The `tidak_pernah_bekerja` component being flat despite overall decline reinforces this: cyclical recovery has largely played out; remaining unemployment is structural.

9. **Youth share (15–29) as a leading indicator** — Youth unemployment collectively (15–19 + 20–24 + 25–29) accounts for roughly 60–65% of total national unemployment in 2021, edging down toward 58–60% by 2025. The gradual but slow decline of this share means youth labor market absorption is improving, but remains the dominant policy challenge.

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
  8. **Insights & Interpretation** — Markdown cells explaining what the charts show and why it matters.
  9. **Summary / Conclusions** — Markdown cell summarizing key findings.

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
