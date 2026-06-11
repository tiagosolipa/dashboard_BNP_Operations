# Operations Monitoring Desk
### BNP Paribas Securities Services — Post-Trade Exception Management

🌐 **Live Demo:** https://dashboardbnpoperations.tiagosolipa.workers.dev/

An action-oriented operational workstation for post-trade exception management. Built as a prototype during the BNP Paribas DRIVE Mentoring Programme.

## Overview
Designed for operations teams who need to triage and resolve issues in real time. Unlike the Lifecycle Dashboard, this tool is built for intervention, surfacing SLA breaches, cut-off countdowns, and risk-scored alerts so operators can act before deadlines are missed.

## Features
- **8 Live KPI Cards** — Requiring action, near cut-off, overdue, manual queue, settlement pending, SLA breaches, awaiting confirmation, critical alerts
- **Stage Hotspot Indicators** — Highlights which workflow stage has the highest exception concentration
- **Risk & Alert Monitor** — Prioritized alert table with risk scores (0–100), cut-off times, alert reasons, and one-click action buttons
- **Risk Score Filtering** — Filter alerts by Low / Med / High / V.High / Critical
- **Transaction Register** — Full transaction list with workflow timeline per transaction
- **Activity History** — Per-transaction log of actions taken
- **Role-based profiles** — Switch between Ops Manager and other roles

## Filters
- Asset Type, Client, Cut-Off Window, Cut-Off Time Interval, Workflow Stage

## 📂 How to Run Locally
1. Download the ZIP file of this repository (via the green **Code** button above).
2. Extract the files.
3. Open `index.html` in any web browser.

## Tech Stack
- Java · Python · CSS
- Built with AI-assisted development using Google Antigravity
