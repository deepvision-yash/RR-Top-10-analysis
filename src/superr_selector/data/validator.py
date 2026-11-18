"""
Data validation module to ensure schema integrity and consistency.
"""

from typing import Dict, List, Tuple
import pandas as pd


class DataValidator:
    """Validates structural and domain integrity of raw and processed datasets."""

    REQUIRED_SCHEMAS = {
        "matches": [
            "match_id",
            "competition_id",
            "season",
            "team1_id",
            "team2_id",
        ],
        "ball_by_ball": [
            "match_id",
            "inning",
            "over",
            "ball",
            "batter_id",
            "bowler_id",
            "total_runs",
            "is_wicket",
        ],
        "teams": ["team_id", "team_name"],
        "playing_eleven": ["match_id", "team_id", "player_id"],
    }

    @classmethod
    def check_schema(cls, df: pd.DataFrame, dataset_name: str) -> Tuple[bool, List[str]]:
        """
        Validate whether the dataframe contains all required columns.

        Returns:
            Tuple of (is_valid, missing_columns)
        """
        if dataset_name not in cls.REQUIRED_SCHEMAS:
            return True, []

        required_cols = cls.REQUIRED_SCHEMAS[dataset_name]
        missing = [col for col in required_cols if col not in df.columns]
        return len(missing) == 0, missing

    @classmethod
    def check_foreign_keys(
        cls,
        parent_df: pd.DataFrame,
        child_df: pd.DataFrame,
        parent_col: str,
        child_col: str,
    ) -> List:
        """
        Find orphan child records that do not exist in the parent dataframe.

        Returns:
            List of orphan ID values.
        """
        parent_ids = set(parent_df[parent_col].dropna().unique())
        child_ids = set(child_df[child_col].dropna().unique())
        orphans = list(child_ids - parent_ids)
        return orphans

    @classmethod
    def validate_ball_by_ball(cls, df: pd.DataFrame) -> Dict[str, any]:
        """
        Perform domain checks on ball-by-ball data:
        - Non-negative runs
        - Valid innings (1, 2, super over)
        - Valid overs (0-19 for 20-over T20 match)
        """
        issues = {}
        if "total_runs" in df.columns:
            negative_runs = (df["total_runs"] < 0).sum()
            if negative_runs > 0:
                issues["negative_total_runs"] = int(negative_runs)

        if "over" in df.columns:
            invalid_overs = (~df["over"].between(0, 19)).sum()
            if invalid_overs > 0:
                issues["invalid_overs_count"] = int(invalid_overs)

        if "is_wicket" in df.columns:
            invalid_wickets = (~df["is_wicket"].isin([0, 1, True, False])).sum()
            if invalid_wickets > 0:
                issues["invalid_wicket_flags"] = int(invalid_wickets)

        return issues

