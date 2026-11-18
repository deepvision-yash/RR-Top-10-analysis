# Data Dictionary

Comprehensive schema documentation for all raw and interim datasets in the `data/` directory.

---

## 1. `data/raw/matches.csv`
Contains match-level metadata for IPL and T20 International fixtures.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `match_id` | Integer / String | Unique identifier for the match | `1304047` |
| `competition_id` | String | Identifier linking to `competitions.csv` | `IPL`, `T20I` |
| `season` | Integer / String | Tournament season / year | `2024` |
| `match_date` | Date (YYYY-MM-DD) | Date the match was played | `2024-04-15` |
| `venue` | String | Stadium / Ground name | `Sawai Mansingh Stadium` |
| `city` | String | City where venue is located | `Jaipur` |
| `team1_id` | String | Unique ID / short name of Team 1 | `RR` |
| `team2_id` | String | Unique ID / short name of Team 2 | `CSK` |
| `toss_winner_id`| String | Team ID that won the toss | `RR` |
| `toss_decision` | String | Decision after toss (`bat` or `field`) | `bat` |
| `winner_id` | String | Winning team ID | `RR` |
| `win_by_runs` | Integer | Margin of victory in runs (if bat 1st) | `16` |
| `win_by_wickets`| Integer | Margin of victory in wickets (if bat 2nd)| `0` |
| `player_of_match_id` | String | Player of the Match identifier | `Jos Buttler` |

---

## 2. `data/raw/ball_by_ball.csv`
Granular delivery-level event logs.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `match_id` | Integer / String | Foreign key to `matches.csv` | `1304047` |
| `inning` | Integer | Innings number (1, 2, 3 for Super Over) | `2` |
| `over` | Integer | Over index (0 to 19 for T20) | `18` |
| `ball` | Integer | Ball index within the over (1 to 6+) | `4` |
| `batter_id` | String | Name or unique player ID of the striker | `Sanju Samson` |
| `bowler_id` | String | Name or unique player ID of the bowler | `Jasprit Bumrah` |
| `non_striker_id`| String | Name or unique ID of non-striker | `Shimron Hetmyer` |
| `batsman_runs` | Integer | Runs scored directly off the bat (0–6) | `4` |
| `extra_runs` | Integer | Runs scored via extras | `0` |
| `total_runs` | Integer | `batsman_runs + extra_runs` | `4` |
| `extras_type` | String | Type of extra (`wides`, `noballs`, `legbyes`, `byes`, `none`) | `none` |
| `is_wicket` | Integer / Boolean | Flag indicating if a wicket fell on this ball | `0` |
| `player_dismissed` | String | Name of dismissed player (if any) | `""` |
| `dismissal_kind` | String | Method of dismissal (`bowled`, `caught`, `run out`, etc.) | `""` |
| `fielder_id` | String | Fielder involved in dismissal | `""` |

---

## 3. `data/raw/competitions.csv`
Details of cricket tournaments covered.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `competition_id` | String | Primary Key | `IPL_2024` |
| `competition_name` | String | Full name of the tournament | `Indian Premier League` |
| `season` | Integer / String | Year / Season | `2024` |
| `format` | String | Match format (`T20`) | `T20` |
| `country` | String | Host nation / administrative country | `India` |

---

## 4. `data/raw/teams.csv`
Team registry and short codes.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `team_id` | String | Primary Key / Short code | `RR` |
| `team_name` | String | Full franchise or international team name | `Rajasthan Royals` |
| `team_short_name`| String | Official abbreviation | `RR` |

---

## 5. `data/raw/playing_eleven.csv`
Lineup information for each fixture.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `match_id` | Integer / String | Foreign key to `matches.csv` | `1304047` |
| `team_id` | String | Foreign key to `teams.csv` | `RR` |
| `player_id` | String | Player identifier | `Yashasvi Jaiswal` |
| `batting_position` | Integer | Designated batting position (1–11) | `1` |
| `is_captain` | Boolean / Int | Team captain indicator | `0` |
| `is_wicketkeeper`| Boolean / Int | Designated wicketkeeper indicator | `0` |

---

## 6. `data/raw/competition_team_player_mapping.csv`
Roster mapping across seasons and squads.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `competition_id` | String | Tournament identifier | `IPL_2024` |
| `season` | Integer | Tournament season | `2024` |
| `team_id` | String | Franchise or national team ID | `RR` |
| `player_id` | String | Player name / ID | `Riyan Parag` |
| `role` | String | Primary squad role (`Batter`, `Bowler`, `All-rounder`, `WK-Batter`) | `Batter` |
| `is_captain` | Boolean / Int | Captaincy status | `0` |
| `is_wicketkeeper`| Boolean / Int | Wicketkeeping status | `0` |

