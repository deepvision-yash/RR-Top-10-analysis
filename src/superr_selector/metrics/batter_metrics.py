"""
Metrics calculation for batters in pressure scenarios.
"""

from typing import Optional
import numpy as np
import pandas as pd


class BatterMetricsCalculator:
    """Calculates batting performance metrics under high-pressure vs normal conditions."""

    def __init__(self, min_balls_faced: int = 30):
        self.min_balls_faced = min_balls_faced

    def compute_batter_stats(
        self,
        df: pd.DataFrame,
        pressure_filter: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Compute aggregate batting metrics.

        Args:
            df: Ball-by-ball DataFrame with pressure features.
            pressure_filter: None, 'high' (pressure_index >= 7), or 'low'.
        """
        data = df.copy()
        if pressure_filter == "high" and "is_high_pressure" in data.columns:
            data = data[data["is_high_pressure"] == 1]
        elif pressure_filter == "low" and "is_high_pressure" in data.columns:
            data = data[data["is_high_pressure"] == 0]

        if "batter_id" not in data.columns or data.empty:
            return pd.DataFrame()

        # Grouping by batter
        grouped = data.groupby("batter_id")

        runs = grouped["batsman_runs"].sum()
        balls = grouped["is_legal_ball"].sum() if "is_legal_ball" in data.columns else grouped.size()
        fours = grouped.apply(lambda g: (g["batsman_runs"] == 4).sum())
        sixes = grouped.apply(lambda g: (g["batsman_runs"] == 6).sum())
        dots = grouped.apply(lambda g: (g["batsman_runs"] == 0).sum())
        dismissals = grouped.apply(lambda g: (g["player_dismissed"] == g.name).sum() if "player_dismissed" in g.columns else 0)

        stats = pd.DataFrame({
            "runs": runs,
            "balls_faced": balls,
            "fours": fours,
            "sixes": sixes,
            "dots": dots,
            "dismissals": dismissals,
        })

        # Filter minimum sample
        stats = stats[stats["balls_faced"] >= self.min_balls_faced].copy()

        # Derived metrics
        stats["strike_rate"] = np.where(stats["balls_faced"] > 0, (stats["runs"] / stats["balls_faced"]) * 100.0, 0.0)
        stats["dot_percentage"] = np.where(stats["balls_faced"] > 0, (stats["dots"] / stats["balls_faced"]) * 100.0, 0.0)
        stats["boundary_percentage"] = np.where(
            stats["balls_faced"] > 0,
            ((stats["fours"] + stats["sixes"]) / stats["balls_faced"]) * 100.0,
            0.0
        )
        stats["batting_average"] = np.where(
            stats["dismissals"] > 0,
            stats["runs"] / stats["dismissals"],
            stats["runs"]
        )

        return stats.reset_index()

