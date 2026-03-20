"""loader.py — Parse and load raw BPS unemployment CSVs into DataFrames."""

from pathlib import Path

import pandas as pd

# Raw data directory (never modify files inside this path)
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

# Column names for the 7-column raw layout
_RAW_COLUMNS: list[str] = [
    "age_group",
    "pernah_bekerja_februari",
    "pernah_bekerja_agustus",
    "tidak_pernah_bekerja_februari",
    "tidak_pernah_bekerja_agustus",
    "jumlah_februari",
    "jumlah_agustus",
]

_DEFAULT_YEARS: list[int] = [2021, 2022, 2023, 2024, 2025]


def load_raw_csv(year: int, data_dir: Path | None = None) -> pd.DataFrame:
    """Load a single raw BPS CSV file for the given year.

    Returns a DataFrame with manually assigned column labels.
    The first 5 rows (multi-row headers) are skipped; columns are renamed.
    """
    dir_ = data_dir if data_dir is not None else RAW_DIR
    file = dir_ / f"Pengangguran Menurut Golongan Umur, {year}.csv"

    if not file.exists():
        raise FileNotFoundError(f"CSV file not found: {file}")

    df = pd.read_csv(file, header=None, skiprows=5, dtype=str)

    # Keep only the first 7 columns (guard against trailing commas)
    df = df.iloc[:, : len(_RAW_COLUMNS)]
    df.columns = _RAW_COLUMNS  # type: ignore[assignment]

    # Drop rows where age_group is NaN (blank trailing rows)
    df.dropna(subset=["age_group"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def load_all_years(
    years: list[int] | None = None,
    data_dir: Path | None = None,
) -> dict[int, pd.DataFrame]:
    """Load all raw CSV files and return a dict mapping year → DataFrame."""
    target_years = years if years is not None else _DEFAULT_YEARS
    return {year: load_raw_csv(year, data_dir=data_dir) for year in target_years}
