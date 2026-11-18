"""
Player ranking engine for computing composite pressure selection index.
"""

from typing import Dict, Optional
import numpy as np
import pandas as pd


class PlayerRankingEngine:
    """Computes composite pressure ratings and rankings for batters and bowlers."""

    @staticmethod
    def min_max_normalize(series: pd.Series, invert: bool = False) -> pd.Series:
        """Min-max normalize a series to 0-100 scale."""
        s_min, s_max = series.min(), series.max()
        if s_max == s_min or np.isnan(s_min) or np.isnan(s_max):
            norm = pd.Series(50.0, index=series.index)
        else:
            norm = (series - s_min) / (s_max - s_min) * 100.0

        if invert:
            return 100.0 - norm
        return norm

    def rank_batters(
        self,
        batter_stats: pd.DataFrame,
        weights: Optional[Dict[str, float]] = None
    ) -> pd.DataFrame:
        """
        Rank batters based on pressure performance metrics.

        Default weights:
        - strike_rate: 0.35
        - dot_percentage (inverted): 0.25
        - boundary_percentage: 0.25
        - batting_average: 0.15
        """
        if batter_stats.empty:
            return batter_stats

        df = batter_stats.copy()
        if weights is None:
            weights = {
                "strike_rate": 0.35,
                "dot_percentage": 0.25,
                "boundary_percentage": 0.25,
                "batting_average": 0.15,
            }

        # Normalize components
        df["sr_score"] = self.min_max_normalize(df["strike_rate"])
        df["dot_score"] = self.min_max_normalize(df["dot_percentage"], invert=True)
        df["boundary_score"] = self.min_max_normalize(df["boundary_percentage"])
        df["avg_score"] = self.min_max_normalize(df["batting_average"])

        # Composite score
        df["superr_batter_score"] = (
            df["sr_score"] * weights["strike_rate"]
            + df["dot_score"] * weights["dot_percentage"]
            + df["boundary_score"] * weights["boundary_percentage"]
            + df["avg_score"] * weights["batting_average"]
        ).round(2)

        df["rank"] = df["superr_batter_score"].rank(ascending=False, method="min").astype(int)
        return df.sort_values("rank").reset_index(drop=True)

    def rank_bowlers(
        self,
        bowler_stats: pd.DataFrame,
        weights: Optional[Dict[str, float]] = None
    ) -> pd.DataFrame:
        """
        Rank bowlers based on pressure performance metrics.

        Default weights:
        - economy_rate (inverted): 0.35
        - dot_percentage: 0.25
        - boundary_conceded_percentage (inverted): 0.20
        - wickets: 0.20
        """
        if bowler_stats.empty:
            return bowler_stats

        df = bowler_stats.copy()
        if weights is None:
            weights = {
                "economy_rate": 0.35,
                "dot_percentage": 0.25,
                "boundary_conceded": 0.20,
                "wickets": 0.20,
            }

        df["econ_score"] = self.min_max_normalize(df["economy_rate"], invert=True)
        df["dot_score"] = self.min_max_normalize(df["dot_percentage"])
        df["boundary_score"] = self.min_max_normalize(df["boundary_conceded_percentage"], invert=True)
        df["wickets_score"] = self.min_max_normalize(df["wickets"])

        df["superr_bowler_score"] = (
            df["econ_score"] * weights["economy_rate"]
            + df["dot_score"] * weights["dot_percentage"]
            + df["boundary_score"] * weights["boundary_conceded"]
            + df["wickets_score"] * weights["wickets"]
        ).round(2)

        df["rank"] = df["superr_bowler_score"].rank(ascending=False, method="min").astype(int)
        return df.sort_values("rank").reset_index(drop=True)

