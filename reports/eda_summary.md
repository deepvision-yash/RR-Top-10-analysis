# SupeRR Selector — Exploratory Data Analysis (EDA)

## 1. Project Overview

**Project:** SupeRR Selector — Pressure-Based Cricket Player Performance Analysis

**Objective:** Identify and rank the top 10 batters and top 10 bowlers based on their performance in high-pressure cricket situations compared with their usual performance.

The project uses ball-by-ball cricket data, match information, competition details, player mappings and playing XI records.

---

## 2. Dataset Overview

Six CSV datasets are provided for analysis.

| Dataset | Rows | Columns |
|---|---:|---:|
| ball_by_ball | 200,999 | 33 |
| competition_team_player_mapping | 6,413 | 6 |
| competitions | 141 | 4 |
| matches | 883 | 22 |
| playing_eleven | 28,381 | 9 |
| teams | 353 | 3 |

### Main Dataset Roles

- **ball_by_ball:** Delivery-level information, including batter, bowler, runs, extras, wickets and delivery characteristics.
- **competition_team_player_mapping:** Maps players to teams and competitions.
- **competitions:** Contains competition names, formats and seasons.
- **matches:** Contains match dates, teams, stages, results and match-level information.
- **playing_eleven:** Contains player participation and team-role information.
- **teams:** Contains competition-wise team information.

---

## 3. Initial Data Quality Checks

### 3.1 Missing Values

Important findings from the initial missing-value analysis:

**ball_by_ball.csv**
- `dismissal_type_id`: 190,118 missing values.
- `dismissal_type`: 190,118 missing values.
- `dismissed_player_id`: 190,107 missing values.
- `extras_type`: 189,167 missing values.
- `stroke`: 6,158 missing values.
- `over_or_around`: 407 missing values.
- `delivery_style`: 391 missing values.

**matches.csv**
- `revised_target`: 860 missing values.
- `first_inn_revised_overs`: 858 missing values.
- `second_inn_revised_overs`: 858 missing values.
- `away_team_captain_id`: 45 missing values.
- `home_team_captain_id`: 44 missing values.
- `win_team_id`: 41 missing values.

**playing_eleven.csv**
- `batting_order`: 8,678 missing values.
- `is_captain`: 8,667 missing values.
- `is_wk`: 8,667 missing values.

The other datasets did not contain missing values in the initial check.

### 3.2 Exact Duplicate Records

No exact duplicate rows were found in any of the six datasets.

This does not rule out duplicate IDs or other logical inconsistencies.

---

## 4. Missing-Value Investigation

### 4.1 Wicket Records

Validation results:

| Check | Count |
|---|---:|
| Wickets without dismissal type | 0 |
| Non-wickets with dismissal type | 0 |
| Wickets without dismissed player ID | 1 |

The one wicket record with a missing dismissed-player ID has:

- Match ID: `40709`
- Striker: Hardik Pandya
- Bowler: Shardul Thakur
- Dismissal type: Retire Out
- Delivery runs: 1

**Decision:** Retain the record and flag the missing player ID. Do not invent a dismissed-player ID.

### 4.2 Extras Records

The following extras categories were observed:

| Extras category | Deliveries |
|---|---:|
| Wide | 7,714 |
| Leg byes | 2,748 |
| Overstep | 576 |
| Byes | 529 |
| Other | 264 |
| Penalty | 1 |
| Missing | 189,167 |

The missing `extras_type` values mostly correspond to deliveries with no extras.

Two deliveries have positive extras but missing extras categories:

- Match `17555`: Dawid Malan vs Haris Rauf.
- Match `36097`: Rassie van der Dussen vs Romario Shepherd.

**Decision:** Retain both records and flag their missing extras categories. Do not guess the category.

### 4.3 Playing Eleven

Missing batting order, captain and wicketkeeper fields are concentrated among non-playing records.

- Non-playing records: 8,667.
- Playing records: 19,714.
- Eleven playing records have missing batting order.

**Decision:** Investigate playing records with missing batting order separately before preprocessing.

### 4.4 Matches Without Winners

There are 41 matches without a recorded `win_team_id`.

Their results include abandoned matches, no-result matches and tied matches.

**Decision:** Retain these match records. Do not assign artificial winners.

---

## 5. Boundary and Runs Validation

### 5.1 Boundary Validation

| Validation | Result |
|---|---:|
| Four records | 23,283 |
| Six records | 12,811 |
|



### Over-Level Delivery Sequence Validation

**Total overs examined:** 32,350

| Validation | Result |
|---|---:|
| Overs not starting at delivery 1 | 0 |
| Overs with duplicate delivery numbers | 0 |
| Overs with non-continuous delivery sequences | 0 |
| Total invalid over sequences | 0 |

**Findings:**
- Every recorded over starts with `over_ball_num = 1`.
- Delivery numbers are continuous within every recorded over.
- No duplicate delivery positions were detected.
- Some overs contain more than six recorded deliveries, consistent with the presence of additional deliveries such as wides.

**Conclusion:** The over-level delivery numbering is structurally consistent across the dataset. However, `over_ball_num` and `innings_ball_num` represent recorded-delivery positions and must not be directly interpreted as legal-ball counts.

**Limitation:** Legal-ball classification remains pending validation of the `Overstep`, `other`, and `Penalty` categories.