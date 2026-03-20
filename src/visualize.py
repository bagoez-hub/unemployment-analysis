"""visualize.py — Reusable charting helpers (Matplotlib, Seaborn, Plotly)."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

# Output directory for saved figures
OUTPUTS_DIR = Path(__file__).resolve().parents[1] / "outputs"

# Colorblind-safe palette for Matplotlib / Seaborn
COLORBLIND_PALETTE = "colorblind"

# Ordered period abbreviations for x-axis labels
_PERIOD_ABBR: dict[str, str] = {"Februari": "Feb", "Agustus": "Aug"}
_PERIOD_SORT: dict[str, int] = {"Februari": 0, "Agustus": 1}

SOURCE_NOTE = "Source: BPS — Badan Pusat Statistik (Statistics Indonesia)"


def _sorted_time_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with a stable 'time_label' column ('YYYY-Feb' / 'YYYY-Aug')
    and a '_sort_key' column for deterministic x-axis ordering."""
    df = df.copy()
    period_str = df["period"].astype(str)
    df["time_label"] = df["year"].astype(str) + "-" + period_str.map(_PERIOD_ABBR)
    df["_sort_key"] = df["year"].astype(int) * 10 + period_str.map(_PERIOD_SORT)
    return df


def _save_or_close(fig: plt.Figure, filename: str, save: bool) -> None:
    """Save figure to outputs/ at 150 dpi, then close it."""
    if save:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(OUTPUTS_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_trend_by_age_group(df: pd.DataFrame, save: bool = True) -> None:
    """Plot total unemployment (jumlah) trend over time, one line per age group.

    Uses Seaborn on a Matplotlib figure. Saves PNG to outputs/ at 150 dpi.
    """
    data = _sorted_time_labels(df)
    time_order = (
        data[["time_label", "_sort_key"]]
        .drop_duplicates()
        .sort_values("_sort_key")["time_label"]
        .tolist()
    )

    palette = sns.color_palette(COLORBLIND_PALETTE, n_colors=len(data["age_group"].unique()))

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(
        data=data,
        x="time_label",
        y="jumlah",
        hue="age_group",
        hue_order=sorted(data["age_group"].unique(), key=lambda g: _age_sort_key(g)),
        palette=palette,
        marker="o",
        ax=ax,
    )

    ax.set_xticks(range(len(time_order)))
    ax.set_xticklabels(time_order, rotation=45, ha="right")
    ax.set_title("Unemployment by Age Group Over Time (2021–2025)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Survey Period")
    ax.set_ylabel("Jumlah Pengangguran (Orang)")
    ax.legend(title="Age Group", bbox_to_anchor=(1.01, 1), loc="upper left")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
    fig.text(0.5, -0.02, SOURCE_NOTE, ha="center", fontsize=8, color="gray")
    plt.tight_layout()

    _save_or_close(fig, "trend_by_age_group.png", save)


def plot_feb_vs_aug(df: pd.DataFrame, save: bool = True) -> None:
    """Grouped bar chart comparing February vs. August total unemployment per year.

    Uses Matplotlib/Seaborn. Saves PNG to outputs/ at 150 dpi.
    """
    # Aggregate across all age groups per (year, period)
    agg = (
        df.groupby(["year", "period"], observed=True)["jumlah"]
        .sum()
        .reset_index()
    )
    agg["period"] = agg["period"].astype(str)

    fig, ax = plt.subplots(figsize=(10, 6))
    palette = sns.color_palette(COLORBLIND_PALETTE, n_colors=2)
    sns.barplot(
        data=agg,
        x="year",
        y="jumlah",
        hue="period",
        hue_order=["Februari", "Agustus"],
        palette=palette,
        ax=ax,
    )

    ax.set_title("Total Unemployment: February vs. August per Year (2021–2025)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Jumlah Pengangguran (Orang)")
    ax.legend(title="Survey Period")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
    fig.text(0.5, -0.02, SOURCE_NOTE, ha="center", fontsize=8, color="gray")
    plt.tight_layout()

    _save_or_close(fig, "feb_vs_aug.png", save)


def plot_interactive_trend(df: pd.DataFrame, save: bool = True) -> None:
    """Interactive Plotly line chart of total unemployment by age group over time.

    Saves standalone HTML to outputs/ if save=True.
    """
    data = _sorted_time_labels(df).sort_values("_sort_key")
    fig = px.line(
        data,
        x="time_label",
        y="jumlah",
        color="age_group",
        category_orders={
            "time_label": sorted(data["time_label"].unique(), key=lambda t: data.loc[data["time_label"] == t, "_sort_key"].iloc[0]),
            "age_group": sorted(data["age_group"].unique(), key=lambda g: _age_sort_key(g)),
        },
        markers=True,
        title="Unemployment by Age Group Over Time (2021–2025) — Interactive",
        labels={
            "time_label": "Survey Period",
            "jumlah": "Jumlah Pengangguran (Orang)",
            "age_group": "Age Group",
        },
    )
    fig.update_layout(
        xaxis_title="Survey Period",
        yaxis_title="Jumlah Pengangguran (Orang)",
        legend_title="Age Group",
        annotations=[
            {"text": SOURCE_NOTE, "xref": "paper", "yref": "paper",
             "x": 0.5, "y": -0.12, "showarrow": False, "font": {"size": 10, "color": "gray"}}
        ],
    )
    fig.update_yaxes(tickformat=",")

    if save:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(OUTPUTS_DIR / "interactive_trend.html"))

    fig.show()


def plot_heatmap(df: pd.DataFrame, save: bool = True) -> None:
    """Heatmap of total unemployment (jumlah) — age group (rows) × survey period (columns).

    Uses Seaborn. Saves PNG to outputs/ at 150 dpi.
    """
    data = _sorted_time_labels(df)
    col_order = (
        data[["time_label", "_sort_key"]]
        .drop_duplicates()
        .sort_values("_sort_key")["time_label"]
        .tolist()
    )
    row_order = sorted(data["age_group"].unique(), key=lambda g: _age_sort_key(g))

    pivot = data.pivot_table(
        index="age_group",
        columns="time_label",
        values="jumlah",
        aggfunc="sum",
    )
    pivot = pivot.loc[[r for r in row_order if r in pivot.index], col_order]

    fig, ax = plt.subplots(figsize=(16, 6))
    sns.heatmap(
        pivot,
        ax=ax,
        cmap="YlOrRd",
        fmt=",",
        annot=True,
        linewidths=0.4,
        cbar_kws={"label": "Jumlah Pengangguran (Orang)"},
    )
    ax.set_title(
        "Unemployment Heatmap: Age Group × Survey Period (2021–2025)",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel("Survey Period")
    ax.set_ylabel("Age Group")
    ax.tick_params(axis="x", rotation=45)
    fig.text(0.5, -0.04, SOURCE_NOTE, ha="center", fontsize=8, color="gray")
    plt.tight_layout()

    _save_or_close(fig, "heatmap.png", save)


def _age_sort_key(age_group: str) -> int:
    """Return a numeric sort key for an age group string (e.g. '15-19' → 15)."""
    try:
        return int(age_group.split("-")[0].replace("+", ""))
    except ValueError:
        return 999
