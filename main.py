"""main.py — Entry point: orchestrates loader → transform → visualize pipeline."""

from src.loader import load_all_years
from src.transform import clean_dataframe, combine_all_years, validate_records
from src.visualize import (
    plot_feb_vs_aug,
    plot_heatmap,
    plot_interactive_trend,
    plot_trend_by_age_group,
)


def main() -> None:
    """Run the full unemployment analysis pipeline."""
    raise NotImplementedError("Pipeline not yet implemented.")


if __name__ == "__main__":
    main()
