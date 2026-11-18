"""
Data loader module for loading raw and processed cricket datasets.
"""

from pathlib import Path
from typing import Dict, Optional, Union
import pandas as pd


class DataLoader:
    """Handles loading datasets for cricket pressure analysis."""

    def __init__(self, data_dir: Optional[Union[str, Path]] = None):
        """
        Initialize DataLoader.

        Args:
            data_dir: Path to the root data directory. Defaults to 'data'.
        """
        if data_dir is None:
            # Fallback relative to project structure
            self.data_dir = Path(__file__).resolve().parents[3] / "data"
        else:
            self.data_dir = Path(data_dir)

        self.raw_dir = self.data_dir / "raw"
        self.interim_dir = self.data_dir / "interim"
        self.processed_dir = self.data_dir / "processed"

    def load_raw_csv(self, filename: str, **kwargs) -> pd.DataFrame:
        """Load a CSV file from data/raw/."""
        file_path = self.raw_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Raw data file not found: {file_path}")
        return pd.read_csv(file_path, **kwargs)

    def load_ball_by_ball(self, **kwargs) -> pd.DataFrame:
        """Load ball-by-ball raw dataset."""
        return self.load_raw_csv("ball_by_ball.csv", **kwargs)

    def load_matches(self, **kwargs) -> pd.DataFrame:
        """Load matches raw dataset."""
        return self.load_raw_csv("matches.csv", **kwargs)

    def load_competitions(self, **kwargs) -> pd.DataFrame:
        """Load competitions raw dataset."""
        return self.load_raw_csv("competitions.csv", **kwargs)

    def load_teams(self, **kwargs) -> pd.DataFrame:
        """Load teams raw dataset."""
        return self.load_raw_csv("teams.csv", **kwargs)

    def load_playing_eleven(self, **kwargs) -> pd.DataFrame:
        """Load playing eleven mapping dataset."""
        return self.load_raw_csv("playing_eleven.csv", **kwargs)

    def load_competition_team_player_mapping(self, **kwargs) -> pd.DataFrame:
        """Load competition-team-player mapping dataset."""
        return self.load_raw_csv("competition_team_player_mapping.csv", **kwargs)

    def load_all_raw(self) -> Dict[str, pd.DataFrame]:
        """Load all raw datasets into a dictionary."""
        return {
            "ball_by_ball": self.load_ball_by_ball(),
            "matches": self.load_matches(),
            "competitions": self.load_competitions(),
            "teams": self.load_teams(),
            "playing_eleven": self.load_playing_eleven(),
            "mapping": self.load_competition_team_player_mapping(),
        }

    def save_processed(self, df: pd.DataFrame, filename: str, **kwargs) -> Path:
        """Save a processed DataFrame to data/processed/."""
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        out_path = self.processed_dir / filename
        if filename.endswith(".parquet"):
            df.to_parquet(out_path, **kwargs)
        else:
            df.to_csv(out_path, index=False, **kwargs)
        return out_path

