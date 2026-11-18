# supeRR Selector: Pressure Analysis Methodology

## 1. Executive Overview
The **supeRR Selector Pressure Analysis** framework is designed to evaluate, quantify, and rank T20 cricket players (IPL and T20 Internationals) specifically on their performance during high-leverage and high-pressure match situations. Standard aggregate metrics (such as overall strike rate or raw bowling average) often obscure a player's true reliability when the game is on the line.

---

## 2. Match Pressure Quantification Model

### 2.1 The Ball-by-Ball Pressure Index ($P_i$)
For every legal ball $i$ in a match, a Pressure Index $P_i \in [1.0, 10.0]$ is computed based on three core dynamics:

$$P_i = \text{Scale}\left(W_{\text{phase}} \times W_{\text{wickets}} \times W_{\text{chase}}\right)$$

Where:
1. **Phase Weight ($W_{\text{phase}}$):**
   - **Powerplay (Overs 1–6):** Base weight $= 1.0$
   - **Middle Overs (Overs 7–15):** Base weight $= 1.2$
   - **Death Overs (Overs 16–20):** Base weight $= 2.0$

2. **Wickets Fallen Weight ($W_{\text{wickets}}$):**
   Reflects the batting side's resource depletion:
   $$W_{\text{wickets}} = 1.0 + \left(\frac{\text{Wickets Down}}{10}\right) \times 1.5$$

3. **Chase Pressure Factor ($W_{\text{chase}}$):**
   Applicable in the 2nd innings based on the Required Run Rate ($\text{RRR}$) relative to Current Run Rate ($\text{CRR}$):
   $$W_{\text{chase}} = \text{clip}\left(\frac{\text{RRR}}{\max(\text{CRR}, 4.0)}, 0.5, 3.0\right)$$
   *(Set to 1.0 during 1st innings)*

### 2.2 Situation Thresholds
- **High Pressure:** $P_i \ge 7.0$ (Top quartile of game-critical deliveries)
- **Moderate Pressure:** $4.0 \le P_i < 7.0$
- **Low Pressure:** $P_i < 4.0$

---

## 3. Batter Evaluation Metrics Under Pressure

When evaluating batters in deliveries where $P_i \ge 7.0$:
- **Pressure Strike Rate ($\text{SR}_P$):** $\frac{\text{Runs Scored}}{\text{Balls Faced}} \times 100$
- **Dot Ball % Under Pressure ($\text{Dot}_P$):** $\frac{\text{Dot Balls}}{\text{Balls Faced}} \times 100$ *(lower is better)*
- **Boundary % ($\text{Bdry}_P$):** $\frac{\text{Fours} + \text{Sixes}}{\text{Balls Faced}} \times 100$
- **Clutch Index ($\text{CI}$):** $\frac{\text{SR}_P}{\text{SR}_{\text{overall}}}$

### Composite Batter Selection Score
$$\text{Score}_{\text{batter}} = 0.35 \times \text{Norm}(\text{SR}_P) + 0.25 \times (100 - \text{Norm}(\text{Dot}_P)) + 0.25 \times \text{Norm}(\text{Bdry}_P) + 0.15 \times \text{Norm}(\text{Avg}_P)$$

---

## 4. Bowler Evaluation Metrics Under Pressure

When evaluating bowlers in deliveries where $P_i \ge 7.0$:
- **Pressure Economy Rate ($\text{Econ}_P$):** $\frac{\text{Runs Conceded}}{\text{Overs Bowled}}$ *(lower is better)*
- **Pressure Dot Ball % ($\text{DotBowler}_P$):** $\frac{\text{Dots Bowled}}{\text{Balls Bowled}} \times 100$
- **Boundary Conceded % ($\text{BdryConceded}_P$):** $\frac{\text{Boundaries Conceded}}{\text{Balls Bowled}} \times 100$ *(lower is better)*
- **Wickets Under Pressure ($W_P$):** Total dismissals executed in high-pressure states

### Composite Bowler Selection Score
$$\text{Score}_{\text{bowler}} = 0.35 \times (100 - \text{Norm}(\text{Econ}_P)) + 0.25 \times \text{Norm}(\text{DotBowler}_P) + 0.20 \times (100 - \text{Norm}(\text{BdryConceded}_P)) + 0.20 \times \text{Norm}(W_P)$$

---

## 5. Player Categorization & Output Tiers
Based on composite scores, players are segmented into 4 actionable squad tiers:
1. **Tier 1 - Elite Clutch:** Consistently outperforms baseline under extreme pressure.
2. **Tier 2 - Reliable Stabilizer:** Dependable anchor, low variance.
3. **Tier 3 - Situational Specialist:** High impact in specific match phases (e.g. death overs only).
4. **Tier 4 - Volatile:** Significant drop-off under pressure ($CI < 0.85$).

