# 📖 Operations Monitoring Desk — Overview & Layout

> **BNP Paribas Securities Services — Post-Trade Exception Management**
>
> 🌐 Live Demo: [https://dashboardbnpoperations.tiagosolipa.workers.dev/](https://dashboardbnpoperations.tiagosolipa.workers.dev/)

---

## What Is This Dashboard?

The Operations Monitoring Desk is an **action-oriented operational workstation** designed for post-trade exception management. It surfaces SLA breaches, cut-off countdowns, and risk-scored alerts so operators can **act before deadlines are missed**.

Unlike passive lifecycle dashboards, this tool is built for **intervention**. Every element — from the KPI cards to the alert table — is clickable and actionable.

---

## Page Layout at a Glance

The dashboard is a **single-page application** organized into the following vertical sections, from top to bottom:

| # | Section | Purpose |
|---|---------|---------|
| 1 | **Header Bar** | Logo, dashboard title, live clock, notifications, user profile |
| 2 | **Filter Bar** | Five global filters + reset button |
| 3 | **KPI Cards** | 8 operational metrics in two rows of 4 |
| 4 | **Stage Hotspot Indicators** | Exception concentration by workflow stage |
| 5 | **Risk & Alert Monitor** | Prioritised alert table with action buttons |
| 6 | **Transaction Register** | Full transaction list with search and pagination |
| 7 | **Transaction Detail Modal** | Pop-up with workflow timeline, metadata, actions, and activity history |

---

## Header Bar

The header spans the full width of the page and contains:

### Logo & Title
- **BNP Paribas Securities Services** logo on the left
- **"Operations Monitoring Desk"** as the primary title
- Subtitle: *"Post-Trade Exception Management · Settlement Monitoring"*

### Live Badge
A green pulsing dot with the text **"Live"**, indicating the dashboard is actively refreshing data.

### Notification Bell 🔔
A bell icon in the header that shows unread notification count. See [05 — Notification System](05-notification-system.md) for full details.

### Live Clock
Displays the current time and date in real time, updated every second.

**Format:** `HH:MM:SS · Day DD Mon`
**Example:** `14:32:08 · Thu 12 Jun`

### User Profile Switcher
Displays the currently active user profile. Clicking it opens a dropdown to switch between available roles.

**Available Profiles:**

| Profile | Initials | Role |
|---------|----------|------|
| **Ops Manager** | OP | Operations Manager |
| **Project Manager** | PM | Project Manager |

**How to switch:**
1. Click the user name/avatar area in the top-right corner
2. A dropdown appears showing all available profiles
3. Click on a profile to switch to it — the active profile is marked with an **"Active"** badge
4. The dropdown closes automatically after switching
5. You can also close it by clicking anywhere outside, or pressing **Escape**

**What changes when you switch profiles:**
- The header avatar initials and name update
- All subsequent actions (approvals, reviews, advances) are logged under the selected profile name
- The Activity History in the transaction modal shows which user performed which action

---

## Filter Bar

The filter bar sits directly below the header and contains **five filter controls** plus a **Reset** button. All filters work together — applying multiple filters narrows down the results cumulatively.

### 1. Asset Type (Chip Buttons)

| Chip | Description |
|------|-------------|
| **All** | Shows all asset types (default) |
| **Cash** | Cash transactions |
| **FX** | Foreign exchange transactions |
| **Derivatives** | Derivative instruments |
| **Money Markets** | Money market transactions |
| **Securities** | Securities transactions |

Click a chip to activate it. The previously active chip is deactivated. Only **one** asset type can be selected at a time.

### 2. Client (Dropdown Select)

A dropdown listing all 15 client names, plus an **"All Clients"** default option. Clients include:

- Allianz Global Investors, BlackRock Asset Mgmt, Amundi Asset Management, AXA Investment Managers, Deutsche Bank AG, HSBC Global Banking, JPMorgan Asset Management, Santander Asset Mgmt, Vanguard Europe, Generali Investments, Aviva Investors, Fidelity International, Pictet Asset Management, Credit Suisse AM, UBS Asset Management

### 3. Cut-Off Window (Chip Buttons)

| Chip | Description |
|------|-------------|
| **All** | No cut-off filter (default) |
| **Overdue** | Only transactions past their cut-off deadline (highlighted in red) |
| **Critical (<2h)** | Only transactions with less than 2 hours to cut-off (highlighted in orange) |
| **Today** | Transactions whose cut-off date is today |
| **Next 24h** | Transactions with cut-off within the next 24 hours |

### 4. Cut-Off Time Interval (Custom Dropdown)

A custom dropdown that filters by the **time of day** of the cut-off deadline:

| Option | Time Range |
|--------|-----------|
| **All Day** | No time restriction (default) |
| **00:00 – 05:00** | Early morning cut-offs |
| **05:00 – 10:00** | Morning cut-offs |
| **10:00 – 14:00** | Mid-day cut-offs |
| **14:00 – 18:00** | Afternoon cut-offs |
| **18:00 – 24:00** | Evening cut-offs |

This dropdown has a custom styled trigger button. Clicking it opens a panel; selecting an option closes the panel and applies the filter.

### 5. Workflow Stage (Dropdown Select)

| Option | Description |
|--------|-------------|
| **All Stages** | No stage filter (default) |
| **Capture** | Transactions in the Capture stage |
| **Confirmation** | Transactions in the Confirmation stage |
| **Settlement** | Transactions in the Settlement stage |
| **Reconciliation** | Transactions in the Reconciliation stage |
| **Completed** | Transactions that have completed their lifecycle |

### ↺ Reset Button

Clicking **"↺ Reset"** clears **all** filters simultaneously and returns the dashboard to its default state:
- All chip buttons reset to "All"
- All dropdowns reset to their default value
- The search box is cleared
- Risk score filter resets to "All"
- KPI card quick-filter is cleared
- Stage error filter is cleared
- Page resets to 1

---

## Auto-Refresh

The dashboard **automatically refreshes every 60 seconds**:
- All risk scores are recalculated based on the current time
- Cut-off countdowns update dynamically
- Overdue durations increase in real time
- KPIs, alerts, and tables re-render with fresh calculations

This means the dashboard is always showing **live, up-to-date** operational data without requiring a manual page refresh.

---

## Data Model

The dashboard generates **400 synthetic transactions** using a deterministic seeded random number generator. The seed is based on the current calendar date, so the data set is consistent within the same day but varies day-to-day.

### Transaction Properties

Each transaction has the following data points:

| Property | Description |
|----------|-------------|
| **Tx ID** | Unique identifier (e.g., `TXN-00042`) |
| **Asset Type** | Cash, FX, Derivatives, Money Markets, or Securities |
| **Client** | One of 15 institutional clients |
| **Client ID** | Unique client code (e.g., `CLI-007`) |
| **Current Stage** | Capture → Confirmation → Settlement → Reconciliation → Completed |
| **Trade Date** | When the trade was executed (rolling window: -4 to +1 days) |
| **Cut-Off** | Deadline for the current stage to complete |
| **Risk Status** | `ok`, `warning`, `critical`, or `overdue` |
| **Risk Score** | 0–100 numeric score |
| **Priority** | `low`, `medium`, or `high` |
| **Manual Intervention** | Whether the transaction requires manual review |
| **STP** | Straight-Through Processing — fully automated (Yes/No) |
| **Notional** | Transaction value in original currency |
| **EUR Equivalent** | Converted value in EUR |
| **Activity History** | Audit trail of all actions taken |

---

## Navigation

📄 **Next:** [02 — KPI Cards & Stage Hotspots](02-kpi-cards-and-stage-hotspots.md)

### Full Table of Contents

1. [Overview & Layout](01-overview-and-layout.md) ← You are here
2. [KPI Cards & Stage Hotspots](02-kpi-cards-and-stage-hotspots.md)
3. [Risk & Alert Monitor](03-risk-and-alert-monitor.md)
4. [Transaction Register](04-transaction-register.md)
5. [Transaction Detail Modal](05-transaction-detail-modal.md)
6. [Notification System](06-notification-system.md)
7. [Risk Score Methodology](07-risk-score-methodology.md)
