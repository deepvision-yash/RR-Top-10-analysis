"""
Unit tests for data preprocessing and cleaner logic.
"""

import pandas as pd
import pytest
from superr_selector.preprocessing.cleaner import DataCleaner


def test_clean_ball_by_ball():
    raw_df = pd.DataFrame({
        "match_id": [1, 1, 1],
        "inning": [1, 1, 1],
        "over": [0, 0, 0],
        "ball": [1, 2, 3],
        "batsman_runs": ["1", None, "4"],
        "extra_runs": [0, 1, 0],
        "total_runs": ["1", "1", "4"],
        "extras_type": [None, "wides", None],
        "is_wicket": ["0", "False", "1"],
    })

    cleaned = DataCleaner.clean_ball_by_ball(raw_df)

    assert cleaned["batsman_runs"].iloc[1] == 0
    assert cleaned["total_runs"].dtype in ["int64", "float64"]
    assert cleaned["is_wicket"].tolist() == [0, 0, 1]
    assert cleaned["extras_type"].iloc[0] == "none"
    assert cleaned["is_legal_ball"].tolist() == [1, 0, 1]


def test_standardize_names():
    names = pd.Series(["  sanju samson ", "Jos Buttler", "YASHASVI JAISWAL "])
    cleaned_names = DataCleaner.standardize_names(names)
    assert cleaned_names.iloc[0] == "Sanju Samson"
    assert cleaned_names.iloc[1] == "Jos Buttler"
    assert cleaned_names.iloc[2] == "Yashasvi Jaiswal"

