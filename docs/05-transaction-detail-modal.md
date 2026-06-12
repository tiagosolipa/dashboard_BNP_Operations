# 🔍 Transaction Detail Modal

> Full transaction deep-dive — metadata, workflow timeline, action buttons, and activity history in a single overlay.

---

## Overview

The Transaction Detail Modal is a **full-screen overlay** that opens when you click any transaction row — either from the Risk & Alert Monitor or the Transaction Register. It provides a complete view of a single transaction, including all metadata, the visual workflow timeline, available actions, and the full activity history.

---

## How to Open the Modal

| Method | Description |
|--------|-------------|
| **Click a row** in the Risk & Alert Monitor table | Opens the modal for that alert's transaction |
| **Click a row** in the Transaction Register table | Opens the modal for that transaction |
| **Click a notification** in the notification dropdown | Opens the modal for the notification's transaction |
| **Click a toast notification** | Opens the modal for the toast's transaction |

---

## How to Close the Modal

| Method | Description |
|--------|-------------|
| **Click the ✕ button** | Top-right corner of the modal |
| **Click outside the modal** | Click the dark overlay background |
| **Press Escape** | Keyboard shortcut |
| **Click an action button** | Some action buttons (in the modal) close the modal after executing |

---

## Modal Layout

The modal is divided into the following sections, from top to bottom:

1. **Modal Header** — Title, subtitle, and close button
2. **Metadata Grid** — 16 data fields in a 4-column grid
3. **Workflow Timeline** — Visual stage progression
4. **Action Buttons** — Available operations for this transaction
5. **Activity History** — Chronological audit trail

---

## 1. Modal Header

| Element | Content |
|---------|---------|
| **Title** | The transaction ID (e.g., "TXN-00042") |
| **Subtitle** | Asset type and client name (e.g., "FX · BlackRock Asset Mgmt") |
| **Close button** | ✕ button on the right |

---

## 2. Metadata Grid

The metadata section displays **16 fields** arranged in a responsive grid (4 columns × 4 rows):

### Row 1 — Identity

| Field | Description | Example |
|-------|-------------|---------|
| **Asset Type** | The asset class of the transaction | "FX" |
| **Client** | Full client name | "BlackRock Asset Mgmt" |
| **Client ID** | Client identifier badge | `CLI-002` |
| **Current Stage** | Colour-coded stage badge | Settlement |

### Row 2 — Risk & Timing

| Field | Description | Example |
|-------|-------------|---------|
| **Risk Status** | Status in uppercase, colour-coded | "OVERDUE" (red), "CRITICAL" (orange), "OK" (green) |
| **⏰ Cut-off Date** | Date portion of the cut-off deadline | "12/06/2026" |
| **⏰ Cut-off Time** | Time portion of the cut-off deadline | "14:30" |
| **Notional** | Transaction value in original currency | "USD 12.5M" |

> **Cut-off styling:** When overdue, both date and time appear in red. When critical, they appear in orange.

### Row 3 — Financial & Priority

| Field | Description | Example |
|-------|-------------|---------|
| **EUR Equivalent** | Converted value in EUR (highlighted) | "€ 11.5M" |
| **Time to Settlement** | Dynamic countdown or overdue duration | "38m to cut-off" or "1h 35m overdue" |
| **Priority** | Priority icon + label + risk score chip | "🔴 High Score: 78/100" |
| **Manual Intervention** | Whether manual review is required | "⚠ Required" or "None" |

> **Priority field:** Includes a clickable **ⓘ** button that opens the Risk Score Explanation Popover (same as in the Alert Monitor). See [07 — Risk Score Methodology](07-risk-score-methodology.md).

### Row 4 — Processing & History

| Field | Description | Example |
|-------|-------------|---------|
| **STP** | Straight-Through Processing status | "✔ STP" (green) or "✖ Non-STP" (red) |
| **Trade Date** | When the trade was executed | "10/06/2026 14:22" |
| **Total Lifecycle** | Total time from first stage entry to now | "18h 45m" |
| **Last Modified By** | User who last acted + timestamp | "Ops Manager · 14:22 · 12/06" |

---

## 3. Workflow Timeline

The Workflow Timeline is a **vertical visual progression** showing all five stages of the transaction lifecycle. Each stage is displayed as a timeline node with colour-coded styling.

### Stages (in order)

| # | Stage | Colour | Icon |
|---|-------|--------|------|
| 1 | **Capture** | Blue (`#1976d2`) | Blue dot |
| 2 | **Confirmation** | Amber (`#f57f17`) | Amber dot |
| 3 | **Settlement** | Red (`#c62828`) | Red dot |
| 4 | **Reconciliation** | Purple (`#7b1fa2`) | Purple dot |
| 5 | **Completed** | Green (`#2e7d32`) | Green dot |

### Timeline Node States

Each stage node appears in one of three states:

#### Completed Stage (transaction has passed through this stage)
- **Coloured dot** — filled with the stage colour
- **Stage name** — in the stage colour
- **Entry timestamp** — when the transaction entered this stage (e.g., "10/06/2026 14:22")
- **Exit timestamp** — when the transaction left this stage
- **Duration** — total time spent in this stage (e.g., "⏱ 2h 15m")

#### Active Stage (transaction is currently in this stage)
- **Coloured dot** — filled with the stage colour
- **Stage name** — in the stage colour
- **Entry timestamp** — when the transaction entered this stage
- **No exit timestamp** — the transaction hasn't left yet
- **Duration** — time spent so far (e.g., "⏱ 45m so far")
- **Active indicator** — a pulsing green dot with text "Currently Active"

#### Future Stage (transaction hasn't reached this stage yet)
- **Grey dot** — unfilled
- **Stage name** — grey, dimmed text
- **"Pending" label** — indicates the stage hasn't been reached
- **Reduced opacity** — the entire node appears at 40% opacity

### Timeline Connections

Each stage node is connected by a vertical line, creating a visual flow from Capture through to Completed. The line styling indicates progress through the workflow.

---

## 4. Action Buttons

Below the workflow timeline, the modal displays **full-width action buttons** for the transaction. These are larger, more descriptive versions of the action buttons in the Alert Monitor.

### Available Actions (for non-completed transactions)

| Button | Appears When | Label | What It Does |
|--------|-------------|-------|-------------|
| **✓ Complete Manual Review** | `manualIntervention === true` | Blue button | Marks the manual review as complete. Clears the manual flag and resolves any alert. |
| **✓ Approve & Advance to Settlement** | `currentStage === "Confirmation"` | Green button | Approves the trade and advances it from Confirmation to Settlement. |
| **⚒ Resolve Alert** | `riskStatus === "overdue"` or `"critical"` | Orange button | Resolves the alert without changing the stage. |
| **→ Advance to Next Stage** | Always (for non-completed) | Grey button | Advances the transaction to the next workflow stage. |

### For Completed Transactions

When the transaction is already completed, instead of action buttons, the modal displays:

> ✓ Transaction Completed & Settled

### Action Button Behaviour

When you click an action button in the modal:

1. The action is executed (transaction data is updated)
2. An **audit log entry** is created under the active user profile
3. A **notification toast** appears confirming the action
4. The **modal closes automatically**
5. The dashboard **re-renders** with updated data

---

## 5. Activity History

The bottom section of the modal shows the **Activity History** (audit trail) — a chronological list of all actions that have been taken on this transaction.

### Header
- **📋 Activity History** — section title with clipboard icon

### Entry Format

Each activity entry displays:

| Element | Description |
|---------|-------------|
| **User avatar** | Coloured circle with user initials (OP or PM) |
| **User name** | Who performed the action (e.g., "Ops Manager") |
| **Timestamp** | When the action was performed (e.g., "14:22 · 12/06") |
| **Action description** | What was done (e.g., "Advanced to Settlement") |
| **Stage transition** | Visual `Previous Stage → New Stage` indicator (only shown when the stage changed) |

### Sorting
- Entries are displayed with **most recent first** (reverse chronological order)
- The newest action is at the top of the list

### Pre-populated History
Each transaction comes pre-populated with synthetic activity history entries representing the automated workflow transitions that occurred before the dashboard was opened. This gives operators context about how the transaction reached its current state.

### User-Generated History
When an operator performs an action (Review, Approve, Resolve, Advance), a new entry is added to the activity history:
- The entry records the **active user profile** (Ops Manager or Project Manager)
- The entry includes the **exact timestamp** of the action
- The entry shows the **previous stage** and **new stage** (if the stage changed)

### Empty State
If a transaction has no activity history (rare — typically only brand-new transactions), the modal shows:

> 📋 No activity recorded yet

---

## Navigation

📄 **Previous:** [04 — Transaction Register](04-transaction-register.md)
📄 **Next:** [06 — Notification System](06-notification-system.md)
