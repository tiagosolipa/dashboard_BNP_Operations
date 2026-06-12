# Operations Monitoring Desk

**BNP Paribas Securities Services — Post-Trade Exception Management**

🌐 **Live Demo:** [https://dashboardbnpoperations.tiagosolipa.workers.dev/](https://dashboardbnpoperations.tiagosolipa.workers.dev/)

---

An action-oriented operational workstation for post-trade exception management. Built as a prototype during the **BNP Paribas DRIVE Mentoring Programme**.

## Overview

Designed for operations teams who need to triage and resolve issues in real time. Unlike the Lifecycle Dashboard, this tool is built for **intervention**, surfacing SLA breaches, cut-off countdowns, and risk-scored alerts so operators can act before deadlines are missed.

## Features

- **8 Live KPI Cards** — Requiring action, near cut-off, overdue, manual queue, settlement pending, SLA breaches, awaiting confirmation, critical alerts
- **Stage Hotspot Indicators** — Highlights which workflow stage has the highest exception concentration
- **Risk & Alert Monitor** — Prioritized alert table with risk scores (0–100), cut-off times, alert reasons, and one-click action buttons
- **Risk Score Filtering** — Filter alerts by Low / Med / High / V.High / Critical
- **Transaction Register** — Full transaction list with workflow timeline per transaction
- **Activity History** — Per-transaction log of actions taken
- **Notification System** — Real-time bell icon notifications and toast pop-ups for overdue, cut-off, and risk alerts
- **Role-based Profiles** — Switch between Ops Manager and Project Manager roles

## Filters

- Asset Type, Client, Cut-Off Window, Cut-Off Time Interval, Workflow Stage

## 📖 Documentation

Detailed feature documentation is available in the [`docs/`](docs/) folder:

| # | Document | Description |
|---|----------|-------------|
| 1 | [Overview & Layout](docs/01-overview-and-layout.md) | Dashboard layout, header, live clock, user profiles, filter bar, and data model |
| 2 | [KPI Cards & Stage Hotspots](docs/02-kpi-cards-and-stage-hotspots.md) | All 8 KPI cards, click-to-filter behaviour, and stage hotspot indicators |
| 3 | [Risk & Alert Monitor](docs/03-risk-and-alert-monitor.md) | Alert table columns, sorting, risk score filtering, and all action buttons |
| 4 | [Transaction Register](docs/04-transaction-register.md) | Full transaction table, search, pagination, columns, and row highlighting |
| 5 | [Transaction Detail Modal](docs/05-transaction-detail-modal.md) | Modal metadata grid, workflow timeline, actions, and activity history |
| 6 | [Notification System](docs/06-notification-system.md) | Bell icon, dropdown, toast pop-ups, all 7 alert types, and deduplication |
| 7 | [Risk Score Methodology](docs/07-risk-score-methodology.md) | Risk score formula, components, thresholds, examples, and dynamic recalculation |

## 📂 How to Run Locally

1. Download the ZIP file of this repository (via the green **Code** button above).
2. Extract the files.
3. Open `index.html` in any web browser.

## Tech Stack

- JavaScript · CSS · HTML
- Built with AI-assisted development using Google Antigravity
