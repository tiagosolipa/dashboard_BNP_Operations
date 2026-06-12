# 📊 Risk Score Methodology

> How the 0–100 risk score is calculated — the formula, components, thresholds, and what drives prioritisation.

---

## Overview

Every transaction in the dashboard is assigned a **Risk Score** between **0 and 100**. This score determines the transaction's **priority level** and its **position** in the Risk & Alert Monitor. Higher scores mean more urgent attention is needed.

The score is **recalculated dynamically** every 60 seconds based on the current time, so it changes in real time as cut-off deadlines approach or pass.

---

## The Formula

```
Risk Score = Time Urgency + Value Weight + Stage Weight
```

The final score is **capped at 100**. Each component contributes a different maximum:

| Component | Max Points | What It Measures |
|-----------|-----------|-----------------|
| **Time Urgency** | 50 pts | How close/past the cut-off deadline |
| **Value Weight** | 30 pts | Financial exposure (notional value in EUR) |
| **Stage Weight** | 20 pts | Which workflow stage — later stages carry more risk |

---

## Component 1: Time Urgency (0–50 points)

The largest contributor to the risk score. Based on the transaction's relationship to its cut-off deadline:

| Condition | Points | Description |
|-----------|--------|-------------|
| **⛔ Overdue** | **50 pts** | Cut-off deadline has passed — transaction is late |
| **⚡ Critical (<2 hours)** | **35 pts** | Less than 2 hours remaining to cut-off |
| **⚠ Warning (2–4 hours)** | **15 pts** | Between 2 and 4 hours remaining to cut-off |
| **✅ On Track (>4 hours)** | **0 pts** | More than 4 hours remaining — no time pressure |

### How risk status is determined from cut-off proximity:

```
minutesToCutoff = (cutoffTime - currentTime) / 60000

if minutesToCutoff < 0        → "overdue"    (50 pts)
if minutesToCutoff < 120      → "critical"   (35 pts)
if minutesToCutoff < 240      → "warning"    (15 pts)
else                          → "ok"         (0 pts)
```

---

## Component 2: Value Weight (0–30 points)

Based on the transaction's notional value converted to EUR. Uses a **logarithmic scale** to prevent extremely large transactions from dominating the score while still giving meaningful weight to value:

```
valueScore = min(30, round(log₁₀(notionalEUR_in_millions + 1) × 20))
```

### Example Values

| Notional (EUR) | log₁₀(M + 1) × 20 | Capped Score |
|---------------|---------------------|-------------|
| €500K (0.5M) | ~3.5 | **4 pts** |
| €1M | ~6.0 | **6 pts** |
| €5M | ~15.6 | **16 pts** |
| €10M | ~20.8 | **21 pts** |
| €20M | ~26.2 | **26 pts** |
| €50M | ~34.2 | **30 pts** (capped) |
| €80M | ~38.0 | **30 pts** (capped) |

The logarithmic curve ensures:
- Small transactions still get some value weight
- Very large transactions don't overwhelm the score — the cap at 30 prevents value alone from driving urgency
- The scale is progressive — each order of magnitude adds roughly the same number of points

---

## Component 3: Stage Weight (0–20 points)

Later stages in the workflow carry more operational risk because more work has been invested and the cost of failure is higher:

| Stage | Points | Rationale |
|-------|--------|-----------|
| **Settlement** | **20 pts** | Highest risk — financial movements are in progress |
| **Reconciliation** | **15 pts** | Post-settlement checks — discrepancies can be costly |
| **Confirmation** | **10 pts** | Trade matching — errors caught here prevent settlement failures |
| **Capture** | **5 pts** | Initial entry — lowest operational exposure |
| **Completed** | **0 pts** | No risk — transaction is finished |

---

## Priority Classification

The final risk score maps to a **priority level** used for display and sorting:

| Priority | Score Range | Icon | Colour |
|----------|-----------|------|--------|
| **High** | 65–100 | 🔴 | Red |
| **Medium** | 35–64 | 🟡 | Yellow/orange |
| **Low** | 0–34 | 🔵 | Blue |

---

## Example Calculations

### Example 1: Overdue Settlement, High Value

| Component | Calculation | Points |
|-----------|-------------|--------|
| Time Urgency | Overdue (past deadline) | 50 |
| Value Weight | €25M → log₁₀(25 + 1) × 20 = 28.3 | 28 |
| Stage Weight | Settlement | 20 |
| **Total** | **Capped at 100** | **98** |
| **Priority** | Score ≥ 65 | 🔴 **HIGH** |

### Example 2: Critical Confirmation, Medium Value

| Component | Calculation | Points |
|-----------|-------------|--------|
| Time Urgency | Critical (45 min to cut-off) | 35 |
| Value Weight | €3M → log₁₀(3 + 1) × 20 = 12.0 | 12 |
| Stage Weight | Confirmation | 10 |
| **Total** | | **57** |
| **Priority** | 35 ≤ Score < 65 | 🟡 **MEDIUM** |

### Example 3: On Track Capture, Low Value

| Component | Calculation | Points |
|-----------|-------------|--------|
| Time Urgency | On track (6 hours to cut-off) | 0 |
| Value Weight | €800K → log₁₀(0.8 + 1) × 20 = 5.1 | 5 |
| Stage Weight | Capture | 5 |
| **Total** | | **10** |
| **Priority** | Score < 35 | 🔵 **LOW** |

---

## Where the Risk Score Appears

The risk score is displayed in several places across the dashboard:

| Location | Format |
|----------|--------|
| **Risk & Alert Monitor table** | Progress bar + numeric value in the "Risk Score" column |
| **Risk & Alert Monitor header** | ⓘ button opens the Risk Score Explanation Popover |
| **Transaction Detail Modal** | "Priority" field shows icon + label + "Score: XX/100" chip |
| **Transaction Detail Modal** | ⓘ button next to Priority opens the same popover |

### Risk Score Explanation Popover

Clicking the **ⓘ** button (either in the Alert Monitor table header or in the modal) opens a floating popover that displays:

1. **Formula:** `Risk Score = Time Urgency + Value Weight + Stage Weight`
2. **Time Urgency breakdown:** All four thresholds with their point values
3. **Value Weight formula:** `log₁₀(Notional €M + 1) × 20`, capped at 30
4. **Stage Weight table:** All five stages with their point values
5. **Footer:** "Final score is capped at 100. Higher = more urgent action needed."

The popover closes when you click anywhere outside of it.

---

## Dynamic Recalculation

The risk score is **not static** — it is recalculated based on the current system time:

| Trigger | Description |
|---------|-------------|
| **Every 60 seconds** | The auto-refresh cycle recalculates all risk data |
| **Before each render** | The `recalculateRiskData()` function runs before any UI update |
| **Before notification scan** | Risk data is refreshed before scanning for new alerts |

### What changes dynamically:
- `minutesToCutoff` decreases in real time as deadlines approach
- A "warning" transaction can become "critical" as it crosses the 2-hour threshold
- A "critical" transaction becomes "overdue" when the deadline passes
- The risk score increases as the time urgency component grows
- Priority can escalate from Low → Medium → High as time passes

### What stays constant:
- Value weight (based on notional value, which doesn't change)
- Stage weight (changes only when an operator advances the stage)

---

## Risk Score Filtering

The Risk & Alert Monitor includes a **risk score filter bar** that lets operators focus on specific score bands:

| Filter | Score Range | Tag |
|--------|-----------|-----|
| All | 0–100 | — |
| 0–30 | 0–30 | Low |
| 31–50 | 31–50 | Med |
| 51–70 | 51–70 | High |
| 71–85 | 71–85 | V.High |
| 86–100 | 86–100 | Critical |

> **Note:** This filter only affects the Alert Monitor table. It does not filter the Transaction Register or the KPI cards.

---

## Navigation

📄 **Previous:** [06 — Notification System](06-notification-system.md)

### Full Table of Contents

1. [Overview & Layout](01-overview-and-layout.md)
2. [KPI Cards & Stage Hotspots](02-kpi-cards-and-stage-hotspots.md)
3. [Risk & Alert Monitor](03-risk-and-alert-monitor.md)
4. [Transaction Register](04-transaction-register.md)
5. [Transaction Detail Modal](05-transaction-detail-modal.md)
6. [Notification System](06-notification-system.md)
7. [Risk Score Methodology](07-risk-score-methodology.md) ← You are here
