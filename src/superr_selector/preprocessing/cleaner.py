"""
Data cleaner module for cleaning and standardizing cricket records.
"""

from typing import Optional
import numpy as np
import pandas as pd


class DataCleaner:
    """Provides methods for cleaning and standardizing raw cricket datasets."""

    @staticmethod
    def clean_ball_by_ball(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean ball-by-ball dataframe:
        - Handle null values in batsman_runs, extra_runs, total_runs
        - Cast numeric types
        - Filter invalid balls/overs
        """
        cleaned = df.copy()

        numeric_cols = ["batsman_runs", "extra_runs", "total_runs", "inning", "over", "ball"]
        for col in numeric_cols:
            if col in cleaned.columns:
                cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce").fillna(0)

        if "is_wicket" in cleaned.columns:
            cleaned["is_wicket"] = (
                cleaned["is_wicket"].astype(str).str.lower().isin(["1", "true", "t"]).astype(int)
            )

        if "extras_type" in cleaned.columns:
            cleaned["extras_type"] = cleaned["extras_type"].fillna("none").astype(str).str.lower()

        # Identify legal deliveries (wides and no-balls do not count as legal balls in standard count)
        if "extras_type" in cleaned.columns:
            cleaned["is_legal_ball"] = (~cleaned["extras_type"].isin(["wides", "noballs"])).astype(int)
        else:
            cleaned["is_legal_ball"] = 1

        return cleaned

    @staticmethod
    def standardize_names(series: pd.Series) -> pd.Series:
        """Strip whitespace and normalize casing for text names."""
        return series.astype(str).str.strip().str.title()

    @staticmethod
    def clean_matches(df: pd.DataFrame) -> pd.DataFrame:
        """Standardize date formats and team columns."""
        cleaned = df.copy()
        if "match_date" in cleaned.columns:
            cleaned["match_date"] = pd.to_datetime(cleaned["match_date"], errors="coerce")
        return cleaned

