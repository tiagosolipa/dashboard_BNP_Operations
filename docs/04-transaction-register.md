# 📋 Transaction Register

> The full transaction list — searchable, filterable, and paginated, with one-click access to transaction details.

---

## Overview

The Transaction Register is a comprehensive table listing **all transactions** in the system. It sits below the Risk & Alert Monitor and responds to all the same global filters. While the Alert Monitor focuses only on exceptions, the Transaction Register shows the complete picture — including healthy, on-track transactions.

---

## Table Header

| Element | Description |
|---------|-------------|
| **Title** | "Transaction Register" |
| **Subtitle** | "Full transaction list · Click any row to view workflow timeline" |
| **Search Input** | Free-text search with placeholder "🔍 Search ID, client, asset..." |
| **Row Count** | Dynamic count showing total matching rows (e.g., "387 rows") |

---

## Search Functionality

The search input provides **real-time filtering** as you type:

- **Debounced input** — there is a 200ms delay after you stop typing before the search executes (to avoid excessive re-renders)
- **Searches across:** Transaction ID, Client name, and Asset type
- **Case-insensitive** — searching "blackrock" will find "BlackRock Asset Mgmt"
- **Partial matching** — searching "TXN-001" will match TXN-00100 through TXN-00199
- **Combines with all other filters** — search works alongside asset type, client, cut-off, stage, and KPI filters

### Examples

| Search Term | Matches |
|-------------|---------|
| `TXN-00042` | Exact transaction ID |
| `BlackRock` | All transactions for BlackRock Asset Mgmt |
| `FX` | All FX transactions |
| `CLI-007` | Won't work — search only covers ID, client name, and asset type |
| `settlement` | Won't match — stage names are not searchable via the text input (use the Stage filter instead) |

---

## Table Columns

The Transaction Register displays **10 columns**:

| # | Column Header | Description |
|---|---------------|-------------|
| 1 | **Tx ID** | Unique transaction identifier (e.g., `TXN-00042`) |
| 2 | **Asset Type** | Colour-coded badge: Cash, FX, Derivatives, Money Markets, or Securities |
| 3 | **Client** | Client name (truncated with ellipsis if too long — max 140px) |
| 4 | **Client ID** | Unique client code badge (e.g., `CLI-007`) |
| 5 | **Current Stage** | Colour-coded badge showing the workflow stage |
| 6 | **Time in Stage** | How long the transaction has been in its current stage |
| 7 | **Cut-Off** | The cut-off deadline (date and time) |
| 8 | **Status** | Risk status with a coloured dot indicator |
| 9 | **Manual** | Whether manual intervention is required |
| 10 | **STP** | Straight-Through Processing status |

---

## Column Details

### Tx ID
The unique identifier for each transaction, displayed as a monospaced text:
- Format: `TXN-XXXXX` (e.g., `TXN-00001` to `TXN-00400`)

### Asset Type Badge

Colour-coded badges:

| Asset | Badge Colour |
|-------|-------------|
| **Cash** | Blue |
| **FX** | Green |
| **Derivatives** | Red/coral |
| **Money Markets** | Teal |
| **Securities** | Purple |

### Client
Full client name. If the name is longer than the column width, it's truncated with an ellipsis (`...`).

### Client ID
A compact badge showing the client's unique code:
- Format: `CLI-XXX` (e.g., `CLI-001` to `CLI-015`)

### Current Stage Badge

| Stage | Badge Colour |
|-------|-------------|
| **Capture** | Blue |
| **Confirmation** | Amber/orange |
| **Settlement** | Red |
| **Reconciliation** | Purple |
| **Completed** | Green |

### Time in Stage
How long the transaction has been in its current workflow stage, formatted as:
- `Xm` for minutes (e.g., "23m")
- `Xh` for exact hours (e.g., "2h")
- `Xh Ym` for hours and minutes (e.g., "1h 45m")
- `0m` if the transaction just entered the stage

Uses tabular numerals for clean alignment in the column.

### Cut-Off
The deadline for the current stage, formatted as `DD/MM/YYYY HH:MM`:

| Status | Display | Styling |
|--------|---------|---------|
| **Overdue** | ⛔ DD/MM/YYYY HH:MM | Red, bold — deadline has passed |
| **Critical** | ⚡ DD/MM/YYYY HH:MM | Orange/amber, bold — less than 2h remaining |
| **Warning** | DD/MM/YYYY HH:MM | Yellow, semi-bold — 2–4h remaining |
| **Ok** | DD/MM/YYYY HH:MM | Normal text |
| **No cut-off** | — | Grey dash |

### Status
Shows the risk status with a coloured dot indicator:

| Status | Dot Colour | Label |
|--------|-----------|-------|
| **Ok** | 🟢 Green | Ok |
| **Warning** | 🟡 Yellow | Warning |
| **Critical** | 🟠 Orange | Critical |
| **Overdue** | 🔴 Red | Overdue |

### Manual
Whether manual intervention is required:

| Value | Display | Styling |
|-------|---------|---------|
| **Yes** | "Yes" | Red/orange highlighted text |
| **No** | "No" | Grey subtle text |

### STP (Straight-Through Processing)
Whether the transaction is processed automatically without human intervention:

| Value | Display | Styling |
|-------|---------|---------|
| **STP** | "STP" | Green text |
| **Non-STP** | "Non-STP" | Red/grey text |

---

## Row Highlighting

Transaction rows are visually highlighted based on their risk status:

| Condition | Row Styling |
|-----------|-------------|
| **Overdue** | Red-tinted background — draws immediate attention |
| **Critical** | Orange/amber-tinted background — urgent |
| **Normal** | Default white/dark background |

---

## Clicking a Row

Clicking any row in the Transaction Register opens the **Transaction Detail Modal** for that transaction. This provides access to:
- Full transaction metadata
- Workflow timeline with timestamps
- Action buttons (review, approve, resolve, advance)
- Activity history / audit trail

See [05 — Transaction Detail Modal](05-transaction-detail-modal.md) for complete details.

---

## Pagination

The Transaction Register supports pagination for large datasets:

| Element | Description |
|---------|-------------|
| **← Prev** button | Navigate to the previous page (disabled on page 1) |
| **Page info** | Shows total transaction count (e.g., "387 transactions") |
| **Next →** button | Navigate to the next page (disabled on the last page) |

- **Page size:** 500 transactions per page
- With 400 total transactions, pagination is rarely needed but is available for filtered views
- The pagination row is **hidden** when all results fit on a single page
- Changing any filter resets the page to 1

---

## Empty State

When no transactions match the current combination of filters, the table displays:

> No transactions match current filters.

This message is centered in the table area with grey styling.

---

## Interaction with Filters

The Transaction Register responds to **all** filter controls:

| Filter | Effect |
|--------|--------|
| **Asset Type chips** | Only shows transactions of the selected asset type |
| **Client dropdown** | Only shows transactions for the selected client |
| **Cut-Off Window chips** | Filters by cut-off urgency (overdue, critical, today, next 24h) |
| **Cut-Off Time Interval** | Filters by the time-of-day bucket of the cut-off |
| **Workflow Stage dropdown** | Only shows transactions in the selected stage |
| **KPI card click** | Filters to transactions matching the KPI criteria |
| **Stage Hotspot click** | Filters to transactions in the selected stage |
| **Search input** | Filters by ID, client name, or asset type text match |

All these filters **combine** — selecting Asset = "FX" and Stage = "Settlement" will show only FX transactions currently in the Settlement stage.

---

## Navigation

📄 **Previous:** [03 — Risk & Alert Monitor](03-risk-and-alert-monitor.md)
📄 **Next:** [05 — Transaction Detail Modal](05-transaction-detail-modal.md)
