"""
Metrics calculation for bowlers under match pressure scenarios.
"""

from typing import Optional
import numpy as np
import pandas as pd


class BowlerMetricsCalculator:
    """Calculates bowling performance metrics under high-pressure vs normal conditions."""

    def __init__(self, min_balls_bowled: int = 30):
        self.min_balls_bowled = min_balls_bowled

    def compute_bowler_stats(
        self,
        df: pd.DataFrame,
        pressure_filter: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Compute aggregate bowling metrics.

        Args:
            df: Ball-by-ball DataFrame with pressure features.
            pressure_filter: None, 'high', or 'low'.
        """
        data = df.copy()
        if pressure_filter == "high" and "is_high_pressure" in data.columns:
            data = data[data["is_high_pressure"] == 1]
        elif pressure_filter == "low" and "is_high_pressure" in data.columns:
            data = data[data["is_high_pressure"] == 0]

        if "bowler_id" not in data.columns or data.empty:
            return pd.DataFrame()

        grouped = data.groupby("bowler_id")

        runs_conceded = grouped["total_runs"].sum()
        legal_balls = grouped["is_legal_ball"].sum() if "is_legal_ball" in data.columns else grouped.size()
        wickets = grouped["is_wicket"].sum() if "is_wicket" in data.columns else 0
        dots = grouped.apply(lambda g: (g["total_runs"] == 0).sum())
        boundaries = grouped.apply(lambda g: (g["total_runs"].isin([4, 6])).sum())

        stats = pd.DataFrame({
            "runs_conceded": runs_conceded,
            "balls_bowled": legal_balls,
            "wickets": wickets,
            "dot_balls": dots,
            "boundaries_conceded": boundaries,
        })

        # Apply minimum sample threshold
        stats = stats[stats["balls_bowled"] >= self.min_balls_bowled].copy()

        # Derived rates
        overs = stats["balls_bowled"] / 6.0
        stats["economy_rate"] = np.where(overs > 0, stats["runs_conceded"] / overs, 0.0)
        stats["dot_percentage"] = np.where(stats["balls_bowled"] > 0, (stats["dot_balls"] / stats["balls_bowled"]) * 100.0, 0.0)
        stats["bowling_strike_rate"] = np.where(stats["wickets"] > 0, stats["balls_bowled"] / stats["wickets"], np.nan)
        stats["boundary_conceded_percentage"] = np.where(
            stats["balls_bowled"] > 0,
            (stats["boundaries_conceded"] / stats["balls_bowled"]) * 100.0,
            0.0
        )

        return stats.reset_index()

