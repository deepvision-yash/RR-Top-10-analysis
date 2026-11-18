# RR IPL 2027 Auction Intelligence — SupeRR Selector Season 2

> **Competition:** SupeRR Selector Season 2 | Round 1 Submission  
> **Team:** Rajasthan Royals (RR) | IPL 2027 Auction Strategy  
> **Methodology:** Pressure Analytics — Ball-by-ball analysis of 18,290 pressure deliveries

---

## Competition Objective

Recommend **Top 10 Batters** + **Top 10 Bowlers** for Rajasthan Royals' IPL 2027 auction strategy using data-driven pressure analytics.

**Pressure Definition:** Required Run Rate >= 15 runs/over AND >= 3 wickets fallen, 2nd innings only  
**Data:** IPL 2022–2026 + International T20I 2022–2026 (200,999 deliveries, 883 matches)

---

## Final Submissions

| File | Description |
|------|-------------|
| `docs/RR_SupeRR_Selector_S2_Submission.pdf` | Full submission document (PDF) |
| `docs/RR_SupeRR_Selector_S2_Submission.md` | Full submission document (Markdown) |
| `reports/tables/SUBMISSION_top10_batters_FINAL.csv` | Final Top 10 Batters |
| `reports/tables/SUBMISSION_top10_bowlers_FINAL.csv` | Final Top 10 Bowlers |

---

## Final Top 10 Batters

| Rank | Player | Nat. | Pressure SR | Boundary% | Pressure Avg | Score |
|------|--------|------|------------|-----------|--------------|-------|
| 1 | Rassie van der Dussen | Overseas | 240.5 | 37.8% | 59.3 | 100.00 |
| 2 | Najibullah Zadran | Overseas | 214.8 | 33.3% | 23.2 | 97.67 |
| 3 | Moeen Ali | Overseas | 195.8 | 30.6% | 25.6 | 95.33 |
| 4 | Evin Lewis | Overseas | 161.9 | 28.6% | 68.0 | 93.00 |
| 5 | Mark Chapman | Overseas | 173.3 | 25.0% | 41.6 | 81.33 |
| 6 | Mahipal Lomror | Indian | 206.5 | 32.3% | 18.3 | 79.00 |
| 7 | Sikandar Raza | Overseas | 175.4 | 23.2% | 26.9 | 72.00 |
| 8 | Reeza Hendricks | Overseas | 170.5 | 27.3% | 21.4 | 69.67 |
| 9 | Prashant Veer | Overseas | 148.4 | 22.6% | 30.7 | 65.00 |
| 10 | Shimron Hetmyer | Overseas | 167.7 | 23.9% | 19.3 | 62.67 |

---

## Final Top 10 Bowlers

| Rank | Player | Nat. | P-Econ | Dot% | P-Wkts | Score |
|------|--------|------|--------|------|--------|-------|
| 1 | Matthew Humphreys | Overseas | 4.31 | 65.6% | 8 | 100.0 |
| 2 | Gerald Coetzee | Overseas | 7.25 | 49.1% | 8 | 98.0 |
| 3 | Umran Malik | Indian | 7.48 | 44.3% | 8 | 92.0 |
| 4 | Taskin Ahmed | Overseas | 7.41 | 43.5% | 7 | 90.0 |
| 5 | Barry McCarthy | Overseas | 7.69 | 45.3% | 6 | 86.0 |
| 6 | Mark Adair | Overseas | 8.05 | 34.3% | 9 | 80.0 |
| 7 | Dasun Shanaka [RR] | Overseas | 8.26 | 47.2% | 7 | 79.5 |
| 8 | Brijesh Sharma [RR] | Indian | 8.20 | 46.7% | 6 | 77.5 |
| 9 | Maheesh Theekshana | Overseas | 8.33 | 37.8% | 13 | 76.0 |
| 10 | Sean Abbott | Overseas | 9.29 | 41.9% | 5 | 57.5 |

> [RR] = Already retained by Rajasthan Royals — no auction cost

---

## Composite Scoring Formula

```
Batters:  35% Pressure SR  +  25% Boundary%  +  20% Pressure Avg
        + 15% Dismissal Control  +  5% Six-hitting

Bowlers:  35% Economy (inv)  +  25% Dot Ball%  +  20% Boundary Conceded (inv)
        + 15% Wickets  +  5% Bowling SR (inv)

Combined = 70% Composite + 30% RR Fit Score
```

All metrics are **percentile-ranked** within the candidate pool — fully data-driven.

---

## Project Structure

```
IPL-RR/
├── data/
│   ├── raw/                        # Official competition dataset (not tracked - large files)
│   └── processed/                  # Intermediate scoring CSVs (not tracked)
├── docs/
│   ├── RR_SupeRR_Selector_S2_Submission.pdf    # FINAL SUBMISSION (PDF)
│   ├── RR_SupeRR_Selector_S2_Submission.md     # FINAL SUBMISSION (Markdown)
│   ├── data_dictionary.md
│   └── methodology.md
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_quality_analysis.ipynb
│   ├── 03_data_preprocessing.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_pressure_analysis.ipynb
│   ├── 06_batter_performance_analysis.ipynb
│   ├── 07_bowler_performance_analysis.ipynb
│   ├── 08_player_ranking.ipynb
│   ├── 09_visualization.ipynb
│   └── 10_rr_auction_intelligence.ipynb        # Main pipeline notebook
├── reports/
│   └── tables/
│       ├── SUBMISSION_top10_batters_FINAL.csv  # Final Top 10 Batters
│       ├── SUBMISSION_top10_bowlers_FINAL.csv  # Final Top 10 Bowlers
│       ├── FINAL_ranked_batters.csv            # Full ranked batter pool (34 players)
│       ├── FINAL_ranked_bowlers.csv            # Full ranked bowler pool (37 players)
│       ├── SET1_auction_batters_T20.csv        # T20 auction batter pool
│       ├── SET1_auction_batters_T20I.csv       # T20I auction batter pool
│       ├── SET1_auction_bowlers_T20.csv        # T20 auction bowler pool
│       ├── SET1_auction_bowlers_T20I.csv       # T20I auction bowler pool
│       ├── SET2_rr_plus_batters_T20.csv        # T20 batter pool incl. RR retained
│       ├── SET2_rr_plus_batters_T20I.csv       # T20I batter pool incl. RR retained
│       ├── SET2_rr_plus_bowlers_T20.csv        # T20 bowler pool incl. RR retained
│       ├── SET2_rr_plus_bowlers_T20I.csv       # T20I bowler pool incl. RR retained
│       ├── A_top50_batters_T20.csv             # Top 50 batters T20
│       ├── A_top50_batters_T20I.csv            # Top 50 batters T20I
│       ├── B_top50_bowlers_T20.csv             # Top 50 bowlers T20
│       ├── B_top50_bowlers_T20I.csv            # Top 50 bowlers T20I
│       ├── C_rr_retained_squad_2027.csv        # RR retained squad reference
│       ├── D_batter_auction_targets.csv        # Batter auction targets
│       ├── D_bowler_auction_targets.csv        # Bowler auction targets
│       ├── E_final_top10_batters_RR.csv
│       ├── F_final_top10_bowlers_RR.csv
│       ├── G_squad_gap_analysis.csv
│       └── H_player_availability_matrix.csv
├── src/superr_selector/            # Python analysis modules
├── tests/                          # Unit tests
├── requirements.txt
└── Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf
```

---

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

> Raw data files (`data/raw/*.csv`) are not tracked due to size. Place the official competition dataset in `data/raw/` before running notebooks.

---

*Analysis: Pressure Analytics Pipeline v3 | Dataset: Official SupeRR Selector Season 2 competition data | All 10 IPL franchise retentions verified*
