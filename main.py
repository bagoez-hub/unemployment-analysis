"""main.py — Entry point: orchestrates loader → transform → visualize pipeline."""

from pathlib import Path

from src.loader import load_all_years
from src.transform import clean_dataframe, combine_all_years, validate_records
from src.visualize import (
    plot_feb_vs_aug,
    plot_heatmap,
    plot_interactive_trend,
    plot_trend_by_age_group,
)

PROCESSED_DIR = Path(__file__).resolve().parent / "data" / "processed"
PROCESSED_FILE = PROCESSED_DIR / "unemployment_combined.csv"


def main() -> None:
    """Run the full unemployment analysis pipeline."""
    print("Loading raw CSV files...")
    raw_frames = load_all_years()

    print("Cleaning and reshaping data...")
    clean_frames = {year: clean_dataframe(df, year) for year, df in raw_frames.items()}

    print("Combining all years...")
    combined = combine_all_years(clean_frames)
    print(f"  Combined shape: {combined.shape} (expected 100 rows × 6 columns)")

    print("Validating records with Pydantic...")
    records = validate_records(combined)
    print(f"  {len(records)} records validated successfully.")

    print("Saving processed dataset...")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    combined.to_csv(PROCESSED_FILE, index=False)
    print(f"  Saved to {PROCESSED_FILE}")

    print("Generating visualizations...")
    plot_trend_by_age_group(combined, save=True)
    print("  trend_by_age_group.png saved.")

    plot_feb_vs_aug(combined, save=True)
    print("  feb_vs_aug.png saved.")

    plot_heatmap(combined, save=True)
    print("  heatmap.png saved.")

    plot_interactive_trend(combined, save=True)
    print("  interactive_trend.html saved.")

    print("Pipeline complete.")


if __name__ == "__main__":
    main()
