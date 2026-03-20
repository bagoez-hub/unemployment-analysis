"""conftest.py — Shared pytest configuration and fixtures."""

import matplotlib

# Force non-interactive backend before any pyplot import so tests run headlessly
matplotlib.use("Agg")

from pathlib import Path  # noqa: E402

import pandas as pd  # noqa: E402
import pytest  # noqa: E402

FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURE_YEAR = 9999


@pytest.fixture()
def fixture_dir() -> Path:
    """Return path to the tests/fixtures/ directory."""
    return FIXTURES_DIR


@pytest.fixture()
def raw_df(fixture_dir: Path) -> pd.DataFrame:
    """Load the raw fixture DataFrame (year 9999) via loader."""
    from src.loader import load_raw_csv

    return load_raw_csv(FIXTURE_YEAR, data_dir=fixture_dir)


@pytest.fixture()
def clean_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Return fixture DataFrame cleaned to long format."""
    from src.transform import clean_dataframe

    return clean_dataframe(raw_df, FIXTURE_YEAR)


@pytest.fixture()
def minimal_df() -> pd.DataFrame:
    """Minimal long-format DataFrame for visualize tests (no file I/O needed)."""
    rows = []
    age_groups = ["15-19", "20-24", "25-29"]
    years = [2021, 2022]
    periods = ["Februari", "Agustus"]
    for year in years:
        for period in periods:
            for i, ag in enumerate(age_groups):
                pb = (i + 1) * 100 + year
                tpb = (i + 1) * 50 + year
                rows.append(
                    {
                        "year": year,
                        "period": period,
                        "age_group": ag,
                        "pernah_bekerja": pb,
                        "tidak_pernah_bekerja": tpb,
                        "jumlah": pb + tpb,
                    }
                )
    return pd.DataFrame(rows)
