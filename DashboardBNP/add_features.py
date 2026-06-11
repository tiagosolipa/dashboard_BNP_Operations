"""
Add 3 features to the BNP ops dashboard:
1. Errors by Stage panel
2. Risk Score interval filters on alert table
3. Enhanced risk-score notifications (70-85 warning, 86-100 critical)
"""
import re

BASE = r'c:\Users\master\OneDrive - Universidade de Lisboa\DashboardBNP'

# ================================================================
# FEATURE 1 + 2: HTML changes
# ================================================================
html_path = BASE + r'\index.html'
with open(html_path, encoding='utf-8') as f:
    html = f.read()

# Add stage errors panel + risk score chips just before the alerts-section
stage_errors_html = '''
    <!-- STAGE ERRORS PANEL -->
    <div class="stage-errors-panel" id="stageErrorsPanel"></div>

'''

risk_chips_in_alerts = '''      <div class="risk-score-filter-bar" id="riskScoreFilterBar">
        <span class="rs-filter-label">Risk Score:</span>
        <button class="rs-chip rs-chip-all active" data-min="0" data-max="100">All</button>
        <button class="rs-chip" data-min="0" data-max="30">0–30 <span class="rs-chip-tag rs-low">Low</span></button>
        <button class="rs-chip" data-min="31" data-max="50">31–50 <span class="rs-chip-tag rs-med">Med</span></button>
        <button class="rs-chip" data-min="51" data-max="70">51–70 <span class="rs-chip-tag rs-high">High</span></button>
        <button class="rs-chip rs-chip-danger" data-min="71" data-max="85">71–85 <span class="rs-chip-tag rs-vhigh">V.High</span></button>
        <button class="rs-chip rs-chip-critical" data-min="86" data-max="100">86–100 <span class="rs-chip-tag rs-crit">Critical</span></button>
      </div>
'''

# Insert stage errors panel before alerts-section
if 'stage-errors-panel' not in html:
    html = html.replace('    <!-- RISK & ALERT MONITOR', stage_errors_html + '    <!-- RISK & ALERT MONITOR')
    print("Added stage errors panel to HTML")
else:
    print("Stage errors panel already exists")

# Insert risk score chips inside alerts-header (after badge)
if 'riskScoreFilterBar' not in html:
    html = html.replace(
        '        <span class="ops-section-hint">',
        risk_chips_in_alerts + '        <span class="ops-section-hint">'
    )
    print("Added risk score filter chips to HTML")
else:
    print("Risk score chips already exist")

# Add riskScoreFilter state reset in resetFilters button area if needed
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"HTML written: {len(html)} chars")

# ================================================================
# FEATURE 1 + 2: JS changes in dashboard.js
# ================================================================
js_path = BASE + r'\dashboard.js'
with open(js_path, encoding='utf-8') as f:
    js = f.read()

# Add riskScoreFilter to state
if 'riskScoreFilter' not in js:
    js = js.replace(
        "  cutoffTimeFilter: { start: -1, end: -1 }, // -1/-1 = All Day\n};",
        "  cutoffTimeFilter: { start: -1, end: -1 }, // -1/-1 = All Day\n  riskScoreFilter: null, // {min, max} or null for all\n  stageErrFilter: null,  // stage name or null\n};"
    )
    print("Added riskScoreFilter to state")

# Add renderStageErrors function before the risk popover section
stage_errors_fn = '''// \u2500\u2500 Errors by Stage Panel \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
function renderStageErrors(data) {
  const panel = document.getElementById("stageErrorsPanel");
  if (!panel) return;
  const stages = ["Capture","Confirmation","Settlement","Reconciliation"];
  const stageData = stages.map(s => {
    const txs = data.filter(t => t.currentStage === s);
    const errors = txs.filter(t => t.riskStatus==="overdue"||t.riskStatus==="critical"||t.manualIntervention);
    return { stage: s, total: txs.length, errors: errors.length, rate: txs.length > 0 ? Math.round((errors.length/txs.length)*100) : 0 };
  });
  const maxErrors = Math.max(...stageData.map(s => s.errors), 1);
  const STAGE_ICONS = { Capture: "📥", Confirmation: "📋", Settlement: "🏦", Reconciliation: "🔄" };
  panel.innerHTML = stageData.map(s => {
    const isHotspot = s.errors === maxErrors && s.errors > 0;
    const severity = isHotspot ? "stage-err-hotspot" : s.errors > 0 ? "stage-err-warn" : "stage-err-ok";
    const isActive = state.stageErrFilter === s.stage;
    return `<div class="stage-err-item ${severity}${isActive ? " stage-err-active" : ""}" onclick="filterByStageErr('${s.stage}')">
      <div class="stage-err-top">
        <span class="stage-err-icon">${STAGE_ICONS[s.stage]}</span>
        <span class="stage-err-name">${s.stage}</span>
        ${isHotspot ? '<span class="stage-err-hotlabel">HOTSPOT</span>' : ""}
      </div>
      <div class="stage-err-nums">
        <span class="stage-err-count">${s.errors}</span>
        <span class="stage-err-sub">/ ${s.total} txns</span>
        <span class="stage-err-rate ${s.rate > 30 ? "rate-high" : s.rate > 0 ? "rate-med" : "rate-ok"}">${s.rate}%</span>
      </div>
      <div class="stage-err-bar-wrap"><div class="stage-err-bar" style="width:${s.total>0?Math.round((s.errors/s.total)*100):0}%"></div></div>
    </div>`;
  }).join("");
}

function filterByStageErr(stage) {
  state.stageErrFilter = (state.stageErrFilter === stage) ? null : stage;
  if (state.stageErrFilter) {
    state.stageFilter = stage;
    document.getElementById("stageFilter").value = stage;
  } else {
    state.stageFilter = "all";
    document.getElementById("stageFilter").value = "all";
  }
  state.page = 1;
  render();
}

'''

if 'renderStageErrors' not in js:
    js = js.replace(
        "// \u2500\u2500 Risk Score Explanation Popover",
        stage_errors_fn + "// \u2500\u2500 Risk Score Explanation Popover"
    )
    print("Added renderStageErrors function")

# Modify renderAlerts to apply riskScoreFilter
# Find the line: "const shown = alertTxs;" and add filter after it
if 'riskScoreFilter' not in js or 'riskScoreFilter' in js[:js.find('renderAlerts')]:
    old_shown = '  // Show ALL alerts — badge count must match rows displayed\n  const shown = alertTxs;'
    new_shown = '  // Apply risk score filter if set\n  const shown = state.riskScoreFilter\n    ? alertTxs.filter(t => t.riskScore >= state.riskScoreFilter.min && t.riskScore <= state.riskScoreFilter.max)\n    : alertTxs;'
    if old_shown in js:
        js = js.replace(old_shown, new_shown)
        print("Added riskScoreFilter to renderAlerts")
    else:
        print("WARNING: could not find shown= line in renderAlerts")

# Update render() to call renderStageErrors
if 'renderStageErrors' not in js.split('function render()')[1]:
    js = js.replace(
        "  renderKPIs(filtered);\n  renderAlerts(filtered);",
        "  renderKPIs(filtered);\n  renderStageErrors(filtered);\n  renderAlerts(filtered);"
    )
    print("Added renderStageErrors call to render()")

# Add riskScoreFilter event listener and stageErrFilter reset to event listeners section
rs_listener = '''
  // \u2500\u2500 Risk Score Interval Filter chips \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
  const rsFilterBar = document.getElementById("riskScoreFilterBar");
  if (rsFilterBar) {
    rsFilterBar.addEventListener("click", e => {
      const chip = e.target.closest(".rs-chip");
      if (!chip) return;
      rsFilterBar.querySelectorAll(".rs-chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      const min = parseInt(chip.dataset.min), max = parseInt(chip.dataset.max);
      state.riskScoreFilter = (min === 0 && max === 100) ? null : { min, max };
      state.page = 1;
      render();
    });
  }

'''

if 'riskScoreFilterBar' not in js:
    # Add before the cutoff time dropdown listener
    js = js.replace(
        "  // \u2500\u2500 Cut-off time interval dropdown",
        rs_listener + "  // \u2500\u2500 Cut-off time interval dropdown"
    )
    print("Added riskScoreFilter event listener")

# Update resetFilters to reset riskScoreFilter
if 'riskScoreFilter: null' not in js.split('resetFilters')[1][:500]:
    js = js.replace(
        "      stageFilter: \"all\", searchQuery: \"\", kpiFilter: null,",
        "      stageFilter: \"all\", searchQuery: \"\", kpiFilter: null,\n      riskScoreFilter: null, stageErrFilter: null,"
    )
    print("Added riskScoreFilter reset")

# Also reset the risk chips UI in resetFilters
old_reset_end = '    document.getElementById("cutoffTimeLabel").textContent = "All Day";\n    document.getElementById("cutoffTimeDropdown").classList.remove("is-active", "open");\n    document.getElementById("clientFilter").value = "all";\n    document.getElementById("stageFilter").value = "all";\n    document.getElementById("tableSearch").value = "";\n    render();\n  });'
new_reset_end = '    document.getElementById("cutoffTimeLabel").textContent = "All Day";\n    document.getElementById("cutoffTimeDropdown").classList.remove("is-active", "open");\n    document.getElementById("clientFilter").value = "all";\n    document.getElementById("stageFilter").value = "all";\n    document.getElementById("tableSearch").value = "";\n    // Reset risk score chips\n    document.querySelectorAll("#riskScoreFilterBar .rs-chip").forEach(c => c.classList.remove("active"));\n    const allChip = document.querySelector("#riskScoreFilterBar .rs-chip-all");\n    if (allChip) allChip.classList.add("active");\n    render();\n  });'
if 'Reset risk score chips' not in js and old_reset_end in js:
    js = js.replace(old_reset_end, new_reset_end)
    print("Added chip reset to resetFilters")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print(f"JS written: {len(js)} chars, {js.count(chr(10))} lines")

# ================================================================
# FEATURE 3: Notifications.js - enhanced risk score notifications
# ================================================================
notif_path = BASE + r'\notifications.js'
with open(notif_path, encoding='utf-8') as f:
    notif = f.read()

# Add new alert types
old_types = '''    "high-risk":  { icon: "\u26a0",  label: "HIGH RISK",     color: "notif-orange", colorVar: "var(--orange)" },'''
new_types = '''    "high-risk":  { icon: "\u26a0",  label: "HIGH RISK",     color: "notif-orange", colorVar: "var(--orange)" },
    "risk-warn":  { icon: "\ud83d\udfe0", label: "RISK WARNING",  color: "notif-orange", colorVar: "var(--orange)" },
    "risk-crit":  { icon: "\ud83d\udd34", label: "RISK CRITICAL", color: "notif-red",    colorVar: "var(--red)" },'''

if 'risk-warn' not in notif:
    notif = notif.replace(old_types, new_types)
    print("Added risk-warn and risk-crit alert types")

# Replace the single high-risk check with tiered checks
old_risk_check = '''      // 5. High risk score (\u2265 65)
      if (tx.riskScore \u003e= 65 \u0026\u0026 tx.riskStatus !== "ok") {
        var keyRisk = tx.id + ":high-risk";
        if (!firedAlerts.has(keyRisk)) {
          firedAlerts.add(keyRisk);
          newAlerts.push(createNotification(tx.id, "high-risk",
            tx.id + " risk score " + tx.riskScore + "/100 \u2014 " + tx.currentStage + " \u00b7 " + window.formatEUR(tx.notionalEUR)
          ));
        }
      }'''

new_risk_check = '''      // 5a. Critical risk score (86-100) — highest urgency
      if (tx.riskScore >= 86 && tx.riskStatus !== "ok") {
        var keyCrit = tx.id + ":risk-crit";
        if (!firedAlerts.has(keyCrit)) {
          firedAlerts.add(keyCrit);
          newAlerts.push(createNotification(tx.id, "risk-crit",
            tx.id + " requires IMMEDIATE attention (Risk Score: " + tx.riskScore + "/100) — " + tx.currentStage
          ));
        }
      }

      // 5b. High risk score (70-85) — warning
      if (tx.riskScore >= 70 && tx.riskScore < 86 && tx.riskStatus !== "ok") {
        var keyWarn = tx.id + ":risk-warn";
        if (!firedAlerts.has(keyWarn)) {
          firedAlerts.add(keyWarn);
          newAlerts.push(createNotification(tx.id, "risk-warn",
            tx.id + " entered high-risk zone (Risk Score: " + tx.riskScore + ") — " + tx.currentStage + " \u00b7 " + window.formatEUR(tx.notionalEUR)
          ));
        }
      }'''

if 'risk-crit' not in notif:
    notif = notif.replace(old_risk_check, new_risk_check)
    print("Updated notification risk score logic to 2-tier")
else:
    print("Risk notification logic already updated")

with open(notif_path, 'w', encoding='utf-8') as f:
    f.write(notif)
print(f"notifications.js written: {len(notif)} chars")

# ================================================================
# FEATURE 1 + 2: CSS changes
# ================================================================
css_path = BASE + r'\styles.css'
with open(css_path, encoding='utf-8') as f:
    css = f.read()

new_css = '''
/* ── STAGE ERRORS PANEL ──────────────────────────────────── */
.stage-errors-panel {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 14px;
}

.stage-err-item {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px 14px;
  cursor: pointer;
  transition: box-shadow 0.15s, transform 0.15s, border-color 0.15s;
  box-shadow: var(--shadow-sm);
  border-left: 3px solid transparent;
}

.stage-err-item:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.stage-err-hotspot {
  border-left-color: var(--red);
  background: #fffafa;
}

.stage-err-warn {
  border-left-color: var(--orange);
  background: #fffdf8;
}

.stage-err-ok {
  border-left-color: var(--bnp-green);
}

.stage-err-active {
  box-shadow: 0 0 0 2px var(--bnp-green), var(--shadow-md);
}

.stage-err-top {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.stage-err-icon { font-size: 14px; }

.stage-err-name {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-primary);
  flex: 1;
}

.stage-err-hotlabel {
  font-size: 8px;
  font-weight: 800;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  background: var(--red);
  color: white;
  padding: 1px 5px;
  border-radius: 3px;
}

.stage-err-nums {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 5px;
}

.stage-err-count {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

.stage-err-sub {
  font-size: 10px;
  color: var(--text-muted);
  flex: 1;
}

.stage-err-rate {
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 10px;
}

.rate-high { background: var(--red-light); color: var(--red); }
.rate-med  { background: var(--orange-light); color: #b45309; }
.rate-ok   { background: var(--green-light); color: var(--green); }

.stage-err-bar-wrap {
  height: 4px;
  background: var(--border);
  border-radius: 2px;
  overflow: hidden;
}

.stage-err-bar {
  height: 100%;
  background: var(--red);
  border-radius: 2px;
  transition: width 0.4s ease;
}

.stage-err-ok .stage-err-bar { background: var(--bnp-green); }
.stage-err-warn .stage-err-bar { background: var(--orange); }

/* ── RISK SCORE FILTER CHIPS ─────────────────────────────── */
.risk-score-filter-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 0 4px;
  flex-wrap: wrap;
}

.rs-filter-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
  white-space: nowrap;
  margin-right: 2px;
}

.rs-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--white);
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  font-family: inherit;
  transition: all 0.15s;
  font-variant-numeric: tabular-nums;
}

.rs-chip:hover { border-color: var(--bnp-green); color: var(--bnp-green); }

.rs-chip.active {
  background: var(--bnp-green);
  color: white;
  border-color: var(--bnp-green);
}

.rs-chip-danger { border-color: var(--orange); color: #b45309; }
.rs-chip-danger:hover { background: var(--orange-light); }
.rs-chip-danger.active { background: var(--orange); color: white; border-color: var(--orange); }

.rs-chip-critical { border-color: var(--red); color: var(--red); }
.rs-chip-critical:hover { background: var(--red-light); }
.rs-chip-critical.active { background: var(--red); color: white; border-color: var(--red); }

.rs-chip-tag {
  font-size: 8px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 1px 4px;
  border-radius: 3px;
  letter-spacing: 0.3px;
}

.rs-low  { background: #e8f5e9; color: var(--green); }
.rs-med  { background: #e8f1fd; color: var(--blue); }
.rs-high { background: var(--orange-light); color: #b45309; }
.rs-vhigh { background: #fff0e0; color: #c2410c; }
.rs-crit { background: var(--red-light); color: var(--red); }

.rs-chip.active .rs-chip-tag {
  background: rgba(255,255,255,0.25);
  color: white;
}
'''

if 'stage-errors-panel' not in css:
    css += new_css
    print("Added stage errors + risk chips CSS")
else:
    print("CSS already has stage errors styles")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print(f"CSS written: {len(css)} chars")

print("\nAll features implemented successfully!")
