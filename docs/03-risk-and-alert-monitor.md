# ⚠ Risk & Alert Monitor

> The primary operational workspace — a prioritised, actionable alert table for exception management.

---

## Overview

The Risk & Alert Monitor is the **centrepiece of the dashboard**. It displays all transactions that require operator attention, ranked by urgency. Each row represents a transaction with an active alert — either overdue, approaching its cut-off, or requiring manual intervention.

**Key features:**
- Sorted by risk severity (overdue first, then critical, then by risk score)
- Filterable by risk score bands
- One-click action buttons for each alert
- Clickable rows to open the full transaction detail modal
- Displays the last user who acted on each transaction

---

## Table Header

The section header contains:

| Element | Description |
|---------|-------------|
| **Title** | "⚠ Risk & Alert Monitor" |
| **Alert count badge** | Shows the number of currently visible alerts (e.g., "12 alerts") — updates dynamically with filters |
| **Hint text** | "Click any row for details · Action buttons resolve exceptions" |

---

## Risk Score Filter Bar

Directly below the header is a **risk score filter bar** with chip buttons that filter which alerts are displayed based on their numeric risk score:

| Chip | Score Range | Tag Label | Description |
|------|-------------|-----------|-------------|
| **All** | 0–100 | — | Shows all alerts (default) |
| **0–30** | 0–30 | Low | Low-risk alerts |
| **31–50** | 31–50 | Med | Medium-risk alerts |
| **51–70** | 51–70 | High | High-risk alerts |
| **71–85** | 71–85 | V.High | Very high-risk alerts (styled with danger colour) |
| **86–100** | 86–100 | Critical | Critical-risk alerts (styled with critical red colour) |

### How It Works
1. Click a risk score chip to filter the alert table to only show alerts within that score range
2. The alert count badge updates to reflect the filtered count
3. Click the "All" chip to remove the filter
4. Only **one** risk score band can be active at a time
5. This filter applies **only** to the Alert Monitor table — it does not affect the Transaction Register below

---

## Alert Table Columns

The alert table displays the following columns for each alert:

| # | Column | Description |
|---|--------|-------------|
| 1 | **Priority** | Visual indicator with coloured icon and text label |
| 2 | **Transaction** | Tx ID, asset type badge, and client name |
| 3 | **Stage** | Current workflow stage as a coloured badge |
| 4 | **Value (EUR)** | EUR equivalent of the transaction notional value |
| 5 | **Cut-off Date** | The date of the cut-off deadline |
| 6 | **Cut-off Time** | The time of the cut-off deadline |
| 7 | **Alert Reason** | Why this transaction is flagged |
| 8 | **Risk Score** | Numeric score (0–100) with a visual progress bar |
| 9 | **Action** | One-click action buttons |
| 10 | **Last Action By** | Initials of the last user who acted on this transaction |

---

## Column Details

### Priority Column

Each alert has a priority level derived from its risk score:

| Priority | Icon | Risk Score | Label Colour |
|----------|------|------------|-------------|
| **HIGH** | 🔴 | ≥ 65 | Red |
| **MEDIUM** | 🟡 | 35–64 | Orange/yellow |
| **LOW** | 🔵 | < 35 | Blue |

### Transaction Column

Shows three pieces of information stacked:
- **Tx ID** — e.g., `TXN-00052` (bold, clickable)
- **Asset badge** — colour-coded badge showing the asset type (Cash, FX, Derivatives, Money Markets, Securities)
- **Client name** — abbreviated to the first two words of the client name

### Stage Column

The current workflow stage displayed as a colour-coded badge:

| Stage | Badge Colour |
|-------|-------------|
| Capture | Blue |
| Confirmation | Amber/orange |
| Settlement | Red |
| Reconciliation | Purple |
| Completed | Green |

### Value (EUR) Column

The transaction's notional value converted to EUR, formatted as:
- **€ X.XM** for millions (e.g., "€ 12.5M")
- **€ XXK** for thousands (e.g., "€ 500K")

High-priority transactions display the value in a bolder, more prominent style.

### Cut-off Date & Time Columns

The deadline is split into two separate columns for readability:

| Risk Status | Date Format | Time Format | Styling |
|-------------|-------------|-------------|---------|
| **Overdue** | DD/MM/YYYY | HH:MM | **Red text** — deadline has passed |
| **Critical** | DD/MM/YYYY | HH:MM | **Orange text** — deadline approaching |
| **Other** | DD/MM/YYYY | HH:MM | Normal text |
| **No cut-off** | — | — | Dash |

### Alert Reason Column

Explains why the transaction was flagged:

| Reason | Example | Meaning |
|--------|---------|---------|
| **X overdue** | "1h 35m overdue" | Transaction is past its cut-off deadline by the stated duration |
| **X to cut-off** | "38m to cut-off" | Transaction has the stated duration remaining before its deadline |
| **Manual required** | "Manual required" | Transaction requires manual intervention regardless of timing |
| **No cut-off defined** | "No cut-off defined" | Transaction has no assigned cut-off time |

### Risk Score Column

Displays both a **visual progress bar** and the **numeric score**:

- The progress bar fills proportionally to the score (0–100%)
- Bar colour matches the priority: red for high, orange for medium, blue for low
- The numeric score is shown to the right of the bar

Clicking the **ⓘ** button next to the "Risk Score" column header opens a **Risk Score Explanation Popover** that details exactly how the score is calculated. See [07 — Risk Score Methodology](07-risk-score-methodology.md) for the full formula.

### Action Column

Each row has **one or two action buttons** depending on the transaction's state. See the [Action Buttons](#action-buttons) section below for full details.

### Last Action By Column

Shows the initials of the last user who performed an action on this transaction:
- **OP** — Ops Manager (with a coloured dot)
- **PM** — Project Manager (with a coloured dot)
- **—** — No actions taken yet

---

## Alert Table Sorting

Alerts are sorted in the following priority order:

1. **Risk Status** (descending): Overdue → Critical → Warning → Ok
2. **Risk Score** (descending): Highest risk score first
3. **Notional EUR Value** (descending): Highest value first
4. **Stage Importance** (descending): Settlement → Reconciliation → Confirmation → Capture → Completed

This ensures the most urgent, highest-value alerts are always at the top.

---

## Action Buttons

The Action column in each alert row provides **one-click resolution buttons**. The available buttons depend on the transaction's current state:

### ✓ Review

| Property | Value |
|----------|-------|
| **Appears when** | Transaction has `manualIntervention === true` |
| **Button text** | ✓ Review |
| **Button colour** | Blue |
| **What it does** | Marks the manual review as complete |
| **Effect on transaction** | Sets `manualIntervention = false`, suppresses the alert, sets `riskStatus = "ok"`, clears the alert reason |
| **Audit log entry** | "Completed Manual Review" |

---

### ⚒ Resolve

| Property | Value |
|----------|-------|
| **Appears when** | Transaction is overdue or critical AND does NOT require manual intervention |
| **Button text** | ⚒ Resolve |
| **Button colour** | Orange |
| **What it does** | Resolves the alert without advancing the stage |
| **Effect on transaction** | Suppresses the alert, sets `riskStatus = "ok"`, sets `manualIntervention = false`, clears the alert reason |
| **Audit log entry** | "Resolved alert" |

---

### ✓ Approve

| Property | Value |
|----------|-------|
| **Appears when** | Transaction is in the Confirmation stage AND does NOT require manual intervention |
| **Button text** | ✓ Approve |
| **Button colour** | Green |
| **What it does** | Approves the transaction and advances it to the Settlement stage |
| **Effect on transaction** | Advances from Confirmation → Settlement, sets `manualIntervention = false`, records timestamps |
| **Audit log entry** | "Approved transaction" |

---

### → Advance

| Property | Value |
|----------|-------|
| **Appears when** | Always (for non-completed transactions) |
| **Button text** | → |
| **Button colour** | Grey/subtle |
| **What it does** | Advances the transaction to the next workflow stage |
| **Effect on transaction** | Moves to the next stage in the sequence: Capture → Confirmation → Settlement → Reconciliation → Completed |
| **Audit log entry** | "Advanced to [next stage]" |
| **Special behaviour** | If advanced to Completed, the risk status is set to "ok" and all alerts are cleared |

---

### ✓ Done

| Property | Value |
|----------|-------|
| **Appears when** | Transaction stage is Completed |
| **Text** | ✓ Done |
| **Colour** | Grey |
| **Interactive** | No — this is a static label, not a button |

---

## Clicking an Alert Row

Clicking anywhere on an alert row (except the action buttons) opens the **Transaction Detail Modal** for that transaction. See [05 — Transaction Detail Modal](05-transaction-detail-modal.md) for full details.

---

## Empty State

When no active alerts exist (all transactions are within SLA and no manual interventions are required), the alert table displays:

> ✅ No active alerts — all transactions within SLA.

---

## What Happens After an Action

When you click any action button:

1. The transaction data is updated immediately in memory
2. An **audit log entry** is created with the user name, action type, previous state, and new state
3. A **notification toast** appears confirming the action (see [06 — Notification System](06-notification-system.md))
4. The entire dashboard **re-renders** — KPIs update, the alert may disappear from the table, and the Transaction Register updates
5. If the transaction is advanced to Completed, it is removed from the alert table entirely

---

## Navigation

📄 **Previous:** [02 — KPI Cards & Stage Hotspots](02-kpi-cards-and-stage-hotspots.md)
📄 **Next:** [04 — Transaction Register](04-transaction-register.md)
