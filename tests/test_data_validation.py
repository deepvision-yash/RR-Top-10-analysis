"""
Unit tests for data validation logic.
"""

import pandas as pd
import pytest
from superr_selector.data.validator import DataValidator


def test_schema_validation_success():
    df = pd.DataFrame({
        "match_id": [1, 2],
        "competition_id": [101, 101],
        "season": [2024, 2024],
        "team1_id": ["RR", "CSK"],
        "team2_id": ["RCB", "MI"],
    })
    is_valid, missing = DataValidator.check_schema(df, "matches")
    assert is_valid is True
    assert len(missing) == 0


def test_schema_validation_missing_cols():
    df = pd.DataFrame({
        "match_id": [1],
        "competition_id": [101],
    })
    is_valid, missing = DataValidator.check_schema(df, "matches")
    assert is_valid is False
    assert "team1_id" in missing
    assert "season" in missing


def test_validate_ball_by_ball_anomalies():
    df = pd.DataFrame({
        "match_id": [1, 1],
        "inning": [1, 1],
        "over": [2, 25],  # 25 is invalid over for T20
        "ball": [1, 2],
        "total_runs": [1, -4],  # negative runs anomaly
        "is_wicket": [0, 99],  # invalid wicket flag
    })
    issues = DataValidator.validate_ball_by_ball(df)
    assert issues.get("negative_total_runs") == 1
    assert issues.get("invalid_overs_count") == 1
    assert issues.get("invalid_wicket_flags") == 1

