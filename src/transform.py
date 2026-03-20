"""transform.py — Cleaning, reshaping, and Pydantic validation of unemployment data."""

import pandas as pd
from pydantic import BaseModel, field_validator

# Canonical age-group ordering (youngest → oldest)
AGE_GROUP_ORDER: list[str] = [
    "15-19",
    "20-24",
    "25-29",
    "30-34",
    "35-39",
    "40-44",
    "45-49",
    "50-54",
    "55-59",
    "60+",
]

PERIOD_ORDER: list[str] = ["Februari", "Agustus"]


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
    """Clean and reshape a raw single-year DataFrame into long format.

    Input is the 7-column wide DataFrame from load_raw_csv.
    Output is long-format with columns: year, period, age_group,
    pernah_bekerja, tidak_pernah_bekerja, jumlah.
    Total rows are separated out and not included in the returned DataFrame.
    """
    df = df.copy()

    # Separate and discard Total row from age-group rows
    total_mask = df["age_group"].str.strip().str.lower() == "total"
    df = df[~total_mask].copy()

    # Drop fully-null rows
    df.dropna(how="all", inplace=True)

    # Check for unexpected nulls in any remaining row
    if df.isnull().any().any():
        raise ValueError(
            f"Year {year}: unexpected null values detected in data rows:\n"
            f"{df[df.isnull().any(axis=1)]}"
        )

    # Cast all numeric columns to int
    numeric_cols = [c for c in df.columns if c != "age_group"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="raise").astype(int)

    # Build one sub-frame per period then stack
    feb = df[
        [
            "age_group",
            "pernah_bekerja_februari",
            "tidak_pernah_bekerja_februari",
            "jumlah_februari",
        ]
    ].copy()
    feb.columns = ["age_group", "pernah_bekerja", "tidak_pernah_bekerja", "jumlah"]  # type: ignore[assignment]
    feb["period"] = "Februari"

    aug = df[
        [
            "age_group",
            "pernah_bekerja_agustus",
            "tidak_pernah_bekerja_agustus",
            "jumlah_agustus",
        ]
    ].copy()
    aug.columns = ["age_group", "pernah_bekerja", "tidak_pernah_bekerja", "jumlah"]  # type: ignore[assignment]
    aug["period"] = "Agustus"

    long_df = pd.concat([feb, aug], ignore_index=True)
    long_df["year"] = year

    # Reorder to canonical column layout
    long_df = long_df[
        ["year", "period", "age_group", "pernah_bekerja", "tidak_pernah_bekerja", "jumlah"]
    ]

    # Assert the fundamental accounting invariant
    bad = long_df[
        long_df["pernah_bekerja"] + long_df["tidak_pernah_bekerja"] != long_df["jumlah"]
    ]
    if not bad.empty:
        raise ValueError(
            f"Year {year}: pernah_bekerja + tidak_pernah_bekerja != jumlah for rows:\n{bad}"
        )

    # Sort by period order then canonical age-group order
    age_cat = pd.CategoricalDtype(categories=AGE_GROUP_ORDER, ordered=True)
    period_cat = pd.CategoricalDtype(categories=PERIOD_ORDER, ordered=True)
    long_df["age_group"] = long_df["age_group"].astype(age_cat)
    long_df["period"] = long_df["period"].astype(period_cat)
    long_df.sort_values(["year", "period", "age_group"], inplace=True)
    long_df.reset_index(drop=True, inplace=True)

    return long_df


def combine_all_years(frames: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """Stack cleaned per-year DataFrames into a single consolidated DataFrame."""
    combined = pd.concat(list(frames.values()), ignore_index=True)

    # Re-apply categorical dtypes after concat (may be lost during concatenation)
    age_cat = pd.CategoricalDtype(categories=AGE_GROUP_ORDER, ordered=True)
    period_cat = pd.CategoricalDtype(categories=PERIOD_ORDER, ordered=True)
    combined["age_group"] = combined["age_group"].astype(str).astype(age_cat)
    combined["period"] = combined["period"].astype(str).astype(period_cat)

    combined.sort_values(["year", "period", "age_group"], inplace=True)
    combined.reset_index(drop=True, inplace=True)

    return combined


def validate_records(df: pd.DataFrame) -> list[UnemploymentRecord]:
    """Validate each row against the UnemploymentRecord schema.

    Raises ValueError on the first row that fails validation.
    """
    records: list[UnemploymentRecord] = []
    for i, row in df.iterrows():
        try:
            record = UnemploymentRecord(
                year=int(row["year"]),
                period=str(row["period"]),
                age_group=str(row["age_group"]),
                pernah_bekerja=int(row["pernah_bekerja"]),
                tidak_pernah_bekerja=int(row["tidak_pernah_bekerja"]),
                jumlah=int(row["jumlah"]),
            )
            records.append(record)
        except Exception as exc:
            raise ValueError(f"Row {i} failed Pydantic validation: {exc}") from exc
    return records
