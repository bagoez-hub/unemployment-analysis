"""loader.py — Parse and load raw BPS unemployment CSVs into DataFrames."""

from pathlib import Path

import pandas as pd

# Raw data directory (never modify files inside this path)
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def load_raw_csv(year: int) -> pd.DataFrame:
    """Load a single raw BPS CSV file for the given year.

    Returns a DataFrame with manually assigned column labels.
    Multi-row headers are skipped; columns are renamed before returning.
    """
    raise NotImplementedError


def load_all_years(years: list[int] | None = None) -> dict[int, pd.DataFrame]:
    """Load all raw CSV files and return a dict mapping year → DataFrame."""
    raise NotImplementedError
