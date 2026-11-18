"""
Feature engineering for match pressure quantification.
"""

from typing import Optional
import numpy as np
import pandas as pd


class PressureFeatureExtractor:
    """Extracts situational context and computes ball-by-ball pressure indices."""

    @staticmethod
    def assign_phase_of_play(over: int) -> str:
        """
        Assign match phase based on over (0-indexed):
        - Powerplay: overs 0 to 5 (overs 1-6)
        - Middle: overs 6 to 14 (overs 7-15)
        - Death: overs 15 to 19 (overs 16-20)
        """
        if over <= 5:
            return "Powerplay"
        elif over <= 14:
            return "Middle"
        else:
            return "Death"

    def compute_innings_state(self, bbb_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates cumulative runs, cumulative wickets, and current run rate (CRR)
        for each match and innings.
        """
        df = bbb_df.copy()
        sort_cols = ["match_id", "inning", "over", "ball"]
        existing_sort_cols = [c for c in sort_cols if c in df.columns]
        if existing_sort_cols:
            df = df.sort_values(existing_sort_cols)

        # Cumulative runs and wickets
        df["cum_runs"] = df.groupby(["match_id", "inning"])["total_runs"].cumsum()
        df["cum_wickets"] = df.groupby(["match_id", "inning"])["is_wicket"].cumsum()

        # Cumulative legal balls
        legal_col = "is_legal_ball" if "is_legal_ball" in df.columns else "ball"
        df["legal_balls_bowled"] = df.groupby(["match_id", "inning"])[legal_col].cumsum()

        # Current Run Rate (CRR)
        df["current_overs"] = df["legal_balls_bowled"] / 6.0
        df["crr"] = np.where(df["current_overs"] > 0, df["cum_runs"] / df["current_overs"], 0.0)

        # Phase
        if "over" in df.columns:
            df["phase"] = df["over"].apply(self.assign_phase_of_play)

        return df

    def compute_pressure_index(
        self,
        df: pd.DataFrame,
        target_col: Optional[str] = "target_runs"
    ) -> pd.DataFrame:
        """
        Compute dynamic pressure score (0 to 10 scale).

        Pressure factors considered:
        1. Phase weight: Death overs have inherently higher leverage.
        2. Wicket pressure: Fewer wickets in hand elevates pressure exponentially.
        3. Chase pressure: Required Run Rate (RRR) vs CRR in 2nd innings.
        """
        res = df.copy()

        # Phase baseline weight
        phase_weights = {"Powerplay": 1.0, "Middle": 1.2, "Death": 2.0}
        phase_factor = res["phase"].map(phase_weights).fillna(1.0) if "phase" in res.columns else 1.0

        # Wickets down weight: 0-2 wickets down = low, 6+ down = severe
        wickets = res["cum_wickets"] if "cum_wickets" in res.columns else 0
        wicket_pressure = 1.0 + (wickets / 10.0) * 1.5

        # Chase pressure (if target available)
        if target_col in res.columns:
            remaining_runs = np.maximum(res[target_col] - res["cum_runs"], 0)
            remaining_balls = np.maximum(120 - res["legal_balls_bowled"], 1)
            res["rrr"] = (remaining_runs / remaining_balls) * 6.0
            chase_ratio = np.clip(res["rrr"] / np.maximum(res["crr"], 4.0), 0.5, 3.0)
        else:
            chase_ratio = 1.0

        # Combined raw pressure score
        raw_pressure = phase_factor * wicket_pressure * chase_ratio

        # Scale to 0-10 index
        min_p = raw_pressure.min()
        max_p = raw_pressure.max()
        if max_p > min_p:
            res["pressure_index"] = 1.0 + 9.0 * ((raw_pressure - min_p) / (max_p - min_p))
        else:
            res["pressure_index"] = 5.0

        res["is_high_pressure"] = (res["pressure_index"] >= 7.0).astype(int)
        return res

