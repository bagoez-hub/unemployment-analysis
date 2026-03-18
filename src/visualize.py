"""visualize.py — Reusable charting helpers (Matplotlib, Seaborn, Plotly)."""

from pathlib import Path

import pandas as pd

# Output directory for saved figures
OUTPUTS_DIR = Path(__file__).resolve().parents[1] / "outputs"

# Colorblind-safe palette for Matplotlib / Seaborn
COLORBLIND_PALETTE = "colorblind"


def plot_trend_by_age_group(df: pd.DataFrame, save: bool = True) -> None:
    """Plot total unemployment trend over time, grouped by age bracket.

    Uses Matplotlib/Seaborn. Saves PNG to outputs/ at 150 dpi if save=True.
    """
    raise NotImplementedError


def plot_feb_vs_aug(df: pd.DataFrame, save: bool = True) -> None:
    """Bar chart comparing February vs. August unemployment per year.

    Uses Matplotlib/Seaborn. Saves PNG to outputs/ at 150 dpi if save=True.
    """
    raise NotImplementedError


def plot_interactive_trend(df: pd.DataFrame, save: bool = True) -> None:
    """Interactive Plotly line chart of total unemployment by age group over time.

    Saves standalone HTML to outputs/ if save=True.
    """
    raise NotImplementedError


def plot_heatmap(df: pd.DataFrame, save: bool = True) -> None:
    """Heatmap of unemployment counts — age group vs. year/period.

    Uses Seaborn. Saves PNG to outputs/ at 150 dpi if save=True.
    """
    raise NotImplementedError
