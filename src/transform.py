"""transform.py — Cleaning, reshaping, and Pydantic validation of unemployment data."""

import pandas as pd
from pydantic import BaseModel, field_validator


class UnemploymentRecord(BaseModel):
    """Pydantic schema for a single validated unemployment row."""

    year: int
    period: str  # 'Februari' | 'Agustus'
    age_group: str
    pernah_bekerja: int
    tidak_pernah_bekerja: int
    jumlah: int

    @field_validator("period")
    @classmethod
    def period_must_be_valid(cls, v: str) -> str:
        if v not in {"Februari", "Agustus"}:
            raise ValueError(f"period must be 'Februari' or 'Agustus', got '{v}'")
        return v

    @field_validator("jumlah")
    @classmethod
    def jumlah_must_equal_sum(cls, v: int, info: object) -> int:
        data = info.data
        expected = data.get("pernah_bekerja", 0) + data.get("tidak_pernah_bekerja", 0)
        if v != expected:
            raise ValueError(
                f"jumlah ({v}) != pernah_bekerja + tidak_pernah_bekerja ({expected})"
            )
        return v


def clean_dataframe(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Clean and reshape a raw single-year DataFrame into long format."""
    raise NotImplementedError


def combine_all_years(frames: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """Stack cleaned per-year DataFrames into a single consolidated DataFrame."""
    raise NotImplementedError


def validate_records(df: pd.DataFrame) -> list[UnemploymentRecord]:
    """Validate each row against the UnemploymentRecord schema.

    Raises ValueError on the first row that fails validation.
    """
    raise NotImplementedError
