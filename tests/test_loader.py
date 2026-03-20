"""test_loader.py — Unit tests for src/loader.py."""

from pathlib import Path

import pandas as pd
import pytest

from src.loader import _RAW_COLUMNS, load_all_years, load_raw_csv

FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURE_YEAR = 9999


class TestLoadRawCsv:
    def test_returns_dataframe(self) -> None:
        df = load_raw_csv(FIXTURE_YEAR, data_dir=FIXTURES_DIR)
        assert isinstance(df, pd.DataFrame)

    def test_shape(self) -> None:
        df = load_raw_csv(FIXTURE_YEAR, data_dir=FIXTURES_DIR)
        # 10 age-group rows + 1 Total row = 11 rows; 7 columns
        assert df.shape == (11, 7)

    def test_column_names(self) -> None:
        df = load_raw_csv(FIXTURE_YEAR, data_dir=FIXTURES_DIR)
        assert list(df.columns) == _RAW_COLUMNS

    def test_age_group_values(self) -> None:
        df = load_raw_csv(FIXTURE_YEAR, data_dir=FIXTURES_DIR)
        assert "15-19" in df["age_group"].values
        assert "60+" in df["age_group"].values
        assert "Total" in df["age_group"].values

    def test_first_data_row(self) -> None:
        df = load_raw_csv(FIXTURE_YEAR, data_dir=FIXTURES_DIR)
        first = df[df["age_group"] == "15-19"].iloc[0]
        # Values from fixture: pb_feb=100, pb_aug=200, ...
        assert first["pernah_bekerja_februari"] == "100"
        assert first["jumlah_februari"] == "250"

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            load_raw_csv(1900, data_dir=tmp_path)


class TestLoadAllYears:
    def test_returns_dict(self) -> None:
        result = load_all_years(years=[FIXTURE_YEAR], data_dir=FIXTURES_DIR)
        assert isinstance(result, dict)

    def test_keys(self) -> None:
        result = load_all_years(years=[FIXTURE_YEAR], data_dir=FIXTURES_DIR)
        assert list(result.keys()) == [FIXTURE_YEAR]

    def test_values_are_dataframes(self) -> None:
        result = load_all_years(years=[FIXTURE_YEAR], data_dir=FIXTURES_DIR)
        for df in result.values():
            assert isinstance(df, pd.DataFrame)

    def test_multiple_years(self) -> None:
        # Load the same fixture twice under two different year keys
        result = load_all_years(years=[FIXTURE_YEAR], data_dir=FIXTURES_DIR)
        assert len(result) == 1
        assert FIXTURE_YEAR in result
