# 📊 KPI Cards & Stage Hotspot Indicators

> Operational metrics at a glance — click any card to filter the entire dashboard.

---

## KPI Cards Overview

The dashboard displays **8 KPI cards** arranged in **two rows of four**. Each card shows a live count of transactions matching a specific operational condition. The values update automatically every 60 seconds.

### How KPI Card Clicking Works

Every KPI card is **clickable** and acts as a **quick-filter** for the entire dashboard:

1. **Click a KPI card** → the dashboard filters all sections (Alert Monitor, Transaction Register) to show only transactions matching that KPI's criteria
2. **The active card** gets a highlighted border and elevated appearance
3. **All other cards** become dimmed/inactive to indicate they are not the current filter
4. **Click the same card again** → the filter is removed and the dashboard returns to showing all transactions
5. **KPI quick-filters combine** with the filter bar — you can have a KPI filter active alongside asset type, client, and other filters

---

## Row 1 — Urgency KPIs

### ⚡ Requiring Action

| Property | Value |
|----------|-------|
| **Icon** | ⚡ (red background) |
| **Counts** | Transactions that are overdue, critical, OR require manual intervention |
| **Subtitle** | "Overdue, critical or manual" |
| **Click action** | Filters to only transactions where `riskStatus === "overdue"` OR `riskStatus === "critical"` OR `manualIntervention === true` |

This is the **primary urgency metric** — the total number of transactions that need operator attention right now.

---

### ⏰ Near Cut-Off

| Property | Value |
|----------|-------|
| **Icon** | ⏰ (orange background) |
| **Counts** | Non-completed transactions with ≤ 30 minutes to their cut-off deadline |
| **Subtitle** | "<30 min to deadline" |
| **Click action** | Filters to transactions where `currentStage ≠ "Completed"` AND `0 ≤ minutesToCutoff ≤ 30` |

Highlights transactions that are about to breach their SLA — the most time-sensitive items that need immediate attention.

---

### ⛔ Overdue

| Property | Value |
|----------|-------|
| **Icon** | ⛔ (solid red background) |
| **Counts** | Transactions past their cut-off deadline |
| **Subtitle** | "Past SLA deadline" |
| **Click action** | Filters to transactions where `riskStatus === "overdue"` |

These are transactions that have already missed their deadline. They require immediate escalation or resolution.

---

### ✋ Manual Queue

| Property | Value |
|----------|-------|
| **Icon** | ✋ (purple background) |
| **Counts** | Transactions requiring manual intervention |
| **Subtitle** | "Awaiting intervention" |
| **Click action** | Filters to transactions where `manualIntervention === true` |

Transactions that cannot proceed via straight-through processing and require a human operator to review, approve, or manually advance them.

---

## Row 2 — Status KPIs

### ⬡ Settlement Pending

| Property | Value |
|----------|-------|
| **Icon** | ⬡ (amber background) |
| **Counts** | Transactions currently in the Settlement stage |
| **Subtitle** | "In settlement stage" |
| **Click action** | Filters to transactions where `currentStage === "Settlement"` |

---

### 🚨 SLA Breaches

| Property | Value |
|----------|-------|
| **Icon** | 🚨 (red background) |
| **Counts** | Transactions past their SLA deadline (same as Overdue) |
| **Subtitle** | "Past deadline" |
| **Click action** | Filters to transactions where `riskStatus === "overdue"` |

> **Note:** SLA Breaches counts the same transactions as Overdue. Both represent transactions that have gone past their cut-off deadline.

---

### 📋 Awaiting Confirmation

| Property | Value |
|----------|-------|
| **Icon** | 📋 (blue background) |
| **Counts** | Transactions currently in the Confirmation stage |
| **Subtitle** | "Confirmation stage" |
| **Click action** | Filters to transactions where `currentStage === "Confirmation"` |

---

### ⚠ Critical Alerts

| Property | Value |
|----------|-------|
| **Icon** | ⚠ (orange background) |
| **Counts** | Transactions with less than 2 hours to cut-off |
| **Subtitle** | "<2h to cut-off" |
| **Click action** | Filters to transactions where `riskStatus === "critical"` |

---

## Visual Behaviour

### Alert Glow
KPI cards that have a count **greater than zero** for alert-type metrics (Requiring Action, Near Cut-Off, Overdue, Manual Queue, SLA Breaches, Critical Alerts) receive a subtle **alert glow effect** to draw attention.

### Active / Inactive States
When a KPI card is clicked:
- **Active card:** Highlighted with a coloured border and slightly elevated shadow
- **Inactive cards:** Dimmed with reduced opacity so the active card stands out
- **No filter active (default):** All cards display at normal opacity

---

## Stage Hotspot Indicators

Below the KPI cards, the **Stage Hotspot Indicators** panel shows the distribution of exceptions (errors) across each workflow stage. This helps operators identify which part of the pipeline is the biggest bottleneck.

### What Is Displayed

The panel shows **four cards**, one for each active workflow stage:

| Stage | Icon | Description |
|-------|------|-------------|
| **📥 Capture** | 📥 | Trade entry and data capture |
| **📋 Confirmation** | 📋 | Trade confirmation and matching |
| **🏦 Settlement** | 🏦 | Settlement execution |
| **🔄 Reconciliation** | 🔄 | Post-settlement reconciliation |

> **Note:** "Completed" is not shown because completed transactions have no exceptions.

### What Each Card Shows

Each stage card displays:

| Element | Description |
|---------|-------------|
| **Stage name** | With its corresponding icon |
| **Exception count** | Number of transactions in this stage that have an exception (overdue, critical, or manual intervention required) |
| **Total count** | Total number of transactions currently in this stage |
| **Exception rate** | Percentage of transactions in this stage that are exceptions |
| **Progress bar** | Visual bar showing the exception rate |
| **HOTSPOT label** | 🔴 Only shown on the stage with the **highest** number of exceptions |

### Colour Coding

| Condition | Colour | Description |
|-----------|--------|-------------|
| **Hotspot** | Red | The stage with the most exceptions — marked with a "HOTSPOT" badge |
| **Has exceptions** | Orange/amber | Stages with some exceptions but not the highest count |
| **No exceptions** | Green | Stages with zero exceptions |

### Exception Rate Thresholds

| Rate | Visual |
|------|--------|
| **> 30%** | Red badge — high exception concentration |
| **> 0%** | Yellow badge — some exceptions present |
| **0%** | Green badge — all clear |

### Clicking a Stage Hotspot Card

Each card is **clickable** and acts as a filter:

1. **Click a stage card** → the Workflow Stage filter is automatically set to that stage, filtering the entire dashboard
2. **The active card** gets a highlighted border
3. **Other cards** become dimmed
4. **Click the same card again** → the filter is removed and all stages are shown again

This links directly to the Workflow Stage filter in the filter bar — they stay in sync.

---

## Navigation

📄 **Previous:** [01 — Overview & Layout](01-overview-and-layout.md)
📄 **Next:** [03 — Risk & Alert Monitor](03-risk-and-alert-monitor.md)
