# 🔔 Notification System

> Real-time alerts via bell icon dropdown and toast pop-ups — monitors transactions and notifies operators when attention is needed.

---

## Overview

The notification system is an **automated monitoring engine** that runs alongside the dashboard. Every **60 seconds**, it scans all transactions for conditions that require operator attention and generates notifications. Notifications are delivered through two channels:

1. **Bell icon dropdown** — a persistent list of all notifications in the header
2. **Toast pop-ups** — brief slide-in notifications in the bottom-right corner

---

## Bell Icon 🔔

### Location
The bell icon is injected into the **header bar**, positioned between the Live badge and the clock.

### Badge Counter
- When there are **unread notifications**, a red badge appears on the bell icon showing the count
- The badge shows the exact number for counts ≤ 99
- For 100+ unread notifications, it shows **"99+"**
- When there are **no unread** notifications, the badge is hidden
- The bell icon has a subtle animation effect when unread notifications are present

---

## Notification Dropdown

### Opening & Closing

| Action | Effect |
|--------|--------|
| **Click the bell icon** | Toggles the dropdown open/closed |
| **Click outside the dropdown** | Closes the dropdown |
| **Press Escape** | Closes the dropdown |

### Dropdown Header

| Element | Description |
|---------|-------------|
| **Title** | "Notifications" |
| **Unread counter** | Shows "X unread" or "All caught up" when fully read |
| **Mark all read button** | "Mark all read" — marks all notifications as read in one click |

### Notification List

Each notification in the dropdown displays:

| Element | Description |
|---------|-------------|
| **Unread dot** | Blue pulsing dot on the left (only for unread notifications) |
| **Alert icon** | Emoji icon representing the alert type |
| **Alert label** | Type tag (e.g., "OVERDUE", "CUT-OFF 10MIN", "MANUAL") |
| **Transaction ID** | The transaction that triggered the notification |
| **Message** | Descriptive text about the alert |
| **Time** | Relative timestamp (e.g., "Just now", "5m ago", "2h ago", "1d ago") |
| **Read button** | ● (unread) or ✓ (read) — click to toggle read status |

### Notification Colours

Each notification type has a colour-coded left border and accent:

| Type | Colour | Accent |
|------|--------|--------|
| **Overdue / Cut-off 10min / Risk Critical** | 🔴 Red | High urgency |
| **Cut-off 30min / High Risk / Risk Warning** | 🟠 Orange | Medium urgency |
| **Manual** | 🟣 Purple | Attention needed |
| **User Action** | 🟢 Green | Confirmation |

### Notification Interactions

| Action | Effect |
|--------|--------|
| **Click a notification** | Marks it as read, closes the dropdown, and opens the Transaction Detail Modal for that transaction |
| **Click the read button (●)** | Marks only that notification as read without navigating |
| **Click "Mark all read"** | Marks all notifications as read at once |

### Empty State

When there are no notifications, the dropdown shows:

> 🔔 No notifications yet
> Alerts will appear here when transactions need attention

---

## Toast Pop-ups

Toast notifications are brief, slide-in notifications that appear in the **bottom-right corner** of the screen.

### Behaviour

| Property | Value |
|----------|-------|
| **Position** | Bottom-right corner, stacked vertically |
| **Maximum visible** | 4 toasts at a time (oldest is removed when a 5th arrives) |
| **Auto-dismiss** | Each toast disappears after **5 seconds** |
| **Animation** | Slides in from the right, slides out when dismissed |

### Toast Content

Each toast displays:

| Element | Description |
|---------|-------------|
| **Alert icon** | Emoji matching the alert type |
| **Alert label** | Type tag (e.g., "OVERDUE", "CUT-OFF 30MIN") |
| **Transaction ID** | The transaction that triggered the alert |
| **Message** | Descriptive text about the alert |
| **Close button** | × button to manually dismiss |

### Toast Interactions

| Action | Effect |
|--------|--------|
| **Click the toast body** | Marks the notification as read, opens the Transaction Detail Modal, and dismisses the toast |
| **Click the × button** | Dismisses the toast without navigating |
| **Wait 5 seconds** | Toast auto-dismisses |

---

## Alert Types

The notification engine monitors for **7 distinct alert conditions**:

### 1. 🔴 OVERDUE

| Property | Value |
|----------|-------|
| **Trigger** | Transaction has passed its cut-off deadline (`riskStatus === "overdue"`) |
| **Message format** | `"TXN-XXXXX is Xh Ym overdue — [Stage] stage"` |
| **Example** | "TXN-00052 is 1h 35m overdue — Settlement stage" |
| **Colour** | Red |

### 2. ⛔ CUT-OFF 10MIN

| Property | Value |
|----------|-------|
| **Trigger** | Cut-off is within 10 minutes AND transaction is not overdue |
| **Message format** | `"TXN-XXXXX cut-off in X min — [Stage] stage"` |
| **Example** | "TXN-00018 cut-off in 8 min — Confirmation stage" |
| **Colour** | Red |

### 3. ⚡ CUT-OFF 30MIN

| Property | Value |
|----------|-------|
| **Trigger** | Cut-off is between 10 and 30 minutes away |
| **Message format** | `"TXN-XXXXX cut-off in Xm — [Stage] stage"` |
| **Example** | "TXN-00093 cut-off in 22m — Settlement stage" |
| **Colour** | Orange |

### 4. ✋ MANUAL

| Property | Value |
|----------|-------|
| **Trigger** | Transaction requires manual intervention (`manualIntervention === true`) |
| **Message format** | `"TXN-XXXXX requires manual intervention — [Asset] · [Client]"` |
| **Example** | "TXN-00128 requires manual intervention — FX · Deutsche Bank" |
| **Colour** | Purple |

### 5. 🔴 RISK CRITICAL

| Property | Value |
|----------|-------|
| **Trigger** | Risk score is 86–100 AND risk status is not "ok" |
| **Message format** | `"TXN-XXXXX requires IMMEDIATE attention (Risk Score: XX/100) - [Stage]"` |
| **Example** | "TXN-00225 requires IMMEDIATE attention (Risk Score: 92/100) - Settlement" |
| **Colour** | Red |

### 6. ⚠ RISK WARNING

| Property | Value |
|----------|-------|
| **Trigger** | Risk score is 70–85 AND risk status is not "ok" |
| **Message format** | `"TXN-XXXXX entered high-risk zone (Score: XX) - [Stage]"` |
| **Example** | "TXN-00370 entered high-risk zone (Score: 75) - Reconciliation" |
| **Colour** | Orange |

### 7. ✅ ACTION

| Property | Value |
|----------|-------|
| **Trigger** | An operator performs an action (review, approve, resolve, advance) |
| **Message format** | `"[User] — [Action] on TXN-XXXXX"` |
| **Example** | "Ops Manager — Approved transaction on TXN-00018" |
| **Colour** | Green |

> **Note:** Unlike the other alert types, ACTION notifications are not generated by the periodic scanner. They are triggered immediately when an operator clicks an action button.

---

## Deduplication

The notification engine uses a **deduplication system** to prevent the same alert from being fired multiple times:

- Each alert is keyed as `"TXN-XXXXX:alertType"` (e.g., `"TXN-00052:overdue"`)
- Once an alert has been fired for a transaction, it will **not** fire again — even across scan cycles
- This means each transaction can generate **at most one** notification per alert type
- A single transaction can trigger multiple **different** alert types (e.g., both "overdue" and "manual")

---

## Scan Cycle

| Property | Value |
|----------|-------|
| **Initial scan** | 1.5 seconds after page load (to let the dashboard render first) |
| **Periodic scan** | Every 60 seconds |
| **Pre-scan step** | Risk data is recalculated before each scan to ensure accuracy |
| **Skip conditions** | Completed transactions and suppressed alerts are skipped |

---

## Navigation

📄 **Previous:** [05 — Transaction Detail Modal](05-transaction-detail-modal.md)
📄 **Next:** [07 — Risk Score Methodology](07-risk-score-methodology.md)
