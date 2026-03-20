"""test_visualize.py — Unit tests for src/visualize.py."""

from pathlib import Path

import pandas as pd
import pytest

from src.visualize import (
    plot_feb_vs_aug,
    plot_heatmap,
    plot_interactive_trend,
    plot_trend_by_age_group,
)


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    """Minimal long-format DataFrame suitable for all chart functions."""
    rows = []
    age_groups = ["15-19", "20-24", "25-29", "30-34"]
    years = [2021, 2022, 2023]
    periods = ["Februari", "Agustus"]
    for year in years:
        for period in periods:
            for i, ag in enumerate(age_groups):
                pb = (i + 1) * 100 + year * 10
                tpb = (i + 1) * 50 + year * 5
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


class TestPlotTrendByAgeGroup:
    def test_runs_without_error(self, sample_df: pd.DataFrame) -> None:
        plot_trend_by_age_group(sample_df, save=False)

    def test_saves_file(self, sample_df: pd.DataFrame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        import src.visualize as vis

        monkeypatch.setattr(vis, "OUTPUTS_DIR", tmp_path)
        plot_trend_by_age_group(sample_df, save=True)
        assert (tmp_path / "trend_by_age_group.png").exists()


class TestPlotFebVsAug:
    def test_runs_without_error(self, sample_df: pd.DataFrame) -> None:
        plot_feb_vs_aug(sample_df, save=False)

    def test_saves_file(self, sample_df: pd.DataFrame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        import src.visualize as vis

        monkeypatch.setattr(vis, "OUTPUTS_DIR", tmp_path)
        plot_feb_vs_aug(sample_df, save=True)
        assert (tmp_path / "feb_vs_aug.png").exists()


class TestPlotInteractiveTrend:
    def test_runs_without_error(self, sample_df: pd.DataFrame, monkeypatch: pytest.MonkeyPatch) -> None:
        # Suppress fig.show() so we don't open a browser in tests
        import plotly.graph_objects as go

        monkeypatch.setattr(go.Figure, "show", lambda *_args, **_kwargs: None)
        plot_interactive_trend(sample_df, save=False)

    def test_saves_html(self, sample_df: pd.DataFrame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        import plotly.graph_objects as go
        import src.visualize as vis

        monkeypatch.setattr(vis, "OUTPUTS_DIR", tmp_path)
        monkeypatch.setattr(go.Figure, "show", lambda *_args, **_kwargs: None)
        plot_interactive_trend(sample_df, save=True)
        assert (tmp_path / "interactive_trend.html").exists()


class TestPlotHeatmap:
    def test_runs_without_error(self, sample_df: pd.DataFrame) -> None:
        plot_heatmap(sample_df, save=False)

    def test_saves_file(self, sample_df: pd.DataFrame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        import src.visualize as vis

        monkeypatch.setattr(vis, "OUTPUTS_DIR", tmp_path)
        plot_heatmap(sample_df, save=True)
        assert (tmp_path / "heatmap.png").exists()
