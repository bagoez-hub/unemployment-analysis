"""test_transform.py — Unit tests for src/transform.py."""

from pathlib import Path

import pandas as pd
import pytest

from src.loader import load_raw_csv
from src.transform import (
    AGE_GROUP_ORDER,
    PERIOD_ORDER,
    UnemploymentRecord,
    clean_dataframe,
    combine_all_years,
    validate_records,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURE_YEAR = 9999


@pytest.fixture()
def raw_df() -> pd.DataFrame:
    return load_raw_csv(FIXTURE_YEAR, data_dir=FIXTURES_DIR)


@pytest.fixture()
def clean_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    return clean_dataframe(raw_df, FIXTURE_YEAR)


class TestCleanDataframe:
    def test_shape(self, clean_df: pd.DataFrame) -> None:
        # 10 age groups × 2 periods = 20 rows; 6 canonical columns
        assert clean_df.shape == (20, 6)

    def test_columns(self, clean_df: pd.DataFrame) -> None:
        assert list(clean_df.columns) == [
            "year",
            "period",
            "age_group",
            "pernah_bekerja",
            "tidak_pernah_bekerja",
            "jumlah",
        ]

    def test_no_total_row(self, clean_df: pd.DataFrame) -> None:
        assert "Total" not in clean_df["age_group"].values

    def test_year_column(self, clean_df: pd.DataFrame) -> None:
        assert (clean_df["year"] == FIXTURE_YEAR).all()

    def test_periods_present(self, clean_df: pd.DataFrame) -> None:
        periods = set(clean_df["period"].astype(str))
        assert periods == {"Februari", "Agustus"}

    def test_all_age_groups_present(self, clean_df: pd.DataFrame) -> None:
        groups = set(clean_df["age_group"].astype(str))
        assert groups == set(AGE_GROUP_ORDER)

    def test_invariant_holds(self, clean_df: pd.DataFrame) -> None:
        pb = clean_df["pernah_bekerja"]
        tpb = clean_df["tidak_pernah_bekerja"]
        jml = clean_df["jumlah"]
        assert (pb + tpb == jml).all()

    def test_numeric_dtypes(self, clean_df: pd.DataFrame) -> None:
        for col in ("pernah_bekerja", "tidak_pernah_bekerja", "jumlah"):
            assert pd.api.types.is_integer_dtype(clean_df[col]), col

    def test_sorted_by_period_then_age(self, clean_df: pd.DataFrame) -> None:
        periods = clean_df["period"].astype(str).tolist()
        # First 10 rows should be Februari, next 10 Agustus
        assert periods[:10] == ["Februari"] * 10
        assert periods[10:] == ["Agustus"] * 10

    def test_broken_invariant_raises(self, raw_df: pd.DataFrame) -> None:
        bad = raw_df.copy()
        bad.loc[bad["age_group"] == "15-19", "jumlah_februari"] = "999999"
        with pytest.raises(ValueError, match="jumlah"):
            clean_dataframe(bad, FIXTURE_YEAR)


class TestCombineAllYears:
    def test_shape(self, clean_df: pd.DataFrame) -> None:
        combined = combine_all_years({FIXTURE_YEAR: clean_df, FIXTURE_YEAR + 1: clean_df.copy()})
        assert combined.shape == (40, 6)

    def test_columns(self, clean_df: pd.DataFrame) -> None:
        combined = combine_all_years({FIXTURE_YEAR: clean_df})
        assert list(combined.columns) == [
            "year",
            "period",
            "age_group",
            "pernah_bekerja",
            "tidak_pernah_bekerja",
            "jumlah",
        ]

    def test_sorted_output(self, clean_df: pd.DataFrame) -> None:
        y1 = clean_df.copy()
        y2 = clean_df.copy()
        y2["year"] = FIXTURE_YEAR + 1
        combined = combine_all_years({FIXTURE_YEAR: y1, FIXTURE_YEAR + 1: y2})
        assert combined["year"].tolist() == sorted(combined["year"].tolist())

    def test_no_duplicates(self, clean_df: pd.DataFrame) -> None:
        combined = combine_all_years({FIXTURE_YEAR: clean_df})
        dup_count = combined.duplicated(subset=["year", "period", "age_group"]).sum()
        assert dup_count == 0


class TestValidateRecords:
    def test_returns_list_of_records(self, clean_df: pd.DataFrame) -> None:
        records = validate_records(clean_df)
        assert isinstance(records, list)
        assert all(isinstance(r, UnemploymentRecord) for r in records)

    def test_count_matches_rows(self, clean_df: pd.DataFrame) -> None:
        records = validate_records(clean_df)
        assert len(records) == len(clean_df)

    def test_invalid_period_raises(self, clean_df: pd.DataFrame) -> None:
        bad = clean_df.copy()
        bad["period"] = "Maret"
        with pytest.raises(ValueError):
            validate_records(bad)

    def test_invalid_jumlah_raises(self, clean_df: pd.DataFrame) -> None:
        bad = clean_df.copy()
        bad.loc[0, "jumlah"] = bad.loc[0, "jumlah"] + 1  # break invariant
        with pytest.raises(ValueError):
            validate_records(bad)

    def test_record_fields(self, clean_df: pd.DataFrame) -> None:
        records = validate_records(clean_df)
        r = records[0]
        assert r.year == FIXTURE_YEAR
        assert r.period in PERIOD_ORDER
        assert r.age_group in AGE_GROUP_ORDER
        assert r.jumlah == r.pernah_bekerja + r.tidak_pernah_bekerja
