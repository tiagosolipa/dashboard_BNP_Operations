import sys
sys.stdout.reconfigure(encoding='utf-8')

css_path = r'c:\Users\master\OneDrive - Universidade de Lisboa\DashboardBNP\styles.css'
notif_path = r'c:\Users\master\OneDrive - Universidade de Lisboa\DashboardBNP\notifications.js'

# ── Append CSS ──────────────────────────────────────────────
css = open(css_path, encoding='utf-8').read()

new_css = """
/* == STAGE ERRORS PANEL ============================== */
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
  transition: box-shadow 0.15s, transform 0.15s;
  box-shadow: var(--shadow-sm);
  border-left: 3px solid transparent;
}
.stage-err-item:hover { box-shadow: var(--shadow-md); transform: translateY(-1px); }
.stage-err-hotspot  { border-left-color: var(--red); background: #fffafa; }
.stage-err-warn     { border-left-color: var(--orange); background: #fffdf8; }
.stage-err-ok       { border-left-color: var(--bnp-green); }
.stage-err-active   { box-shadow: 0 0 0 2px var(--bnp-green), var(--shadow-md); }
.stage-err-top      { display: flex; align-items: center; gap: 6px; margin-bottom: 6px; }
.stage-err-icon     { font-size: 14px; }
.stage-err-name     { font-size: 11px; font-weight: 700; color: var(--text-primary); flex: 1; }
.stage-err-hotlabel {
  font-size: 8px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;
  background: var(--red); color: white; padding: 1px 5px; border-radius: 3px;
}
.stage-err-nums     { display: flex; align-items: baseline; gap: 4px; margin-bottom: 5px; }
.stage-err-count    { font-size: 20px; font-weight: 800; color: var(--text-primary); font-variant-numeric: tabular-nums; }
.stage-err-sub      { font-size: 10px; color: var(--text-muted); flex: 1; }
.stage-err-rate     { font-size: 10px; font-weight: 700; padding: 1px 6px; border-radius: 10px; }
.rate-high { background: var(--red-light); color: var(--red); }
.rate-med  { background: var(--orange-light); color: #b45309; }
.rate-ok   { background: var(--green-light); color: var(--green); }
.stage-err-bar-wrap { height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; }
.stage-err-bar      { height: 100%; background: var(--red); border-radius: 2px; transition: width 0.4s ease; }
.stage-err-ok   .stage-err-bar  { background: var(--bnp-green); }
.stage-err-warn .stage-err-bar  { background: var(--orange); }

/* == RISK SCORE FILTER CHIPS ========================= */
.risk-score-filter-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px 8px;
  background: var(--bg);
  border-top: 1px solid var(--border-light);
  border-bottom: 1px solid var(--border-light);
  flex-wrap: wrap;
}
.rs-filter-label {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.5px; color: var(--text-muted); white-space: nowrap; margin-right: 2px;
}
.rs-chip {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 4px 10px; border-radius: 20px; border: 1px solid var(--border);
  background: var(--white); font-size: 11px; font-weight: 600;
  color: var(--text-secondary); cursor: pointer; font-family: inherit;
  transition: all 0.15s; font-variant-numeric: tabular-nums;
}
.rs-chip:hover { border-color: var(--bnp-green); color: var(--bnp-green); }
.rs-chip.active { background: var(--bnp-green); color: white; border-color: var(--bnp-green); }
.rs-chip-danger { border-color: var(--orange); color: #b45309; }
.rs-chip-danger:hover { background: var(--orange-light); }
.rs-chip-danger.active { background: var(--orange); color: white; border-color: var(--orange); }
.rs-chip-critical { border-color: var(--red); color: var(--red); }
.rs-chip-critical:hover { background: var(--red-light); }
.rs-chip-critical.active { background: var(--red); color: white; border-color: var(--red); }
.rs-chip-tag {
  font-size: 8px; font-weight: 800; text-transform: uppercase;
  padding: 1px 4px; border-radius: 3px; letter-spacing: 0.3px;
}
.rs-low  { background: #e8f5e9; color: var(--green); }
.rs-med  { background: #e8f1fd; color: var(--blue); }
.rs-high { background: var(--orange-light); color: #b45309; }
.rs-vhigh { background: #fff0e0; color: #c2410c; }
.rs-crit { background: var(--red-light); color: var(--red); }
.rs-chip.active .rs-chip-tag { background: rgba(255,255,255,0.25); color: white; }
"""

if 'stage-err-item' not in css:
    css += new_css
    print("CSS: added new styles")
else:
    print("CSS: styles already present")

open(css_path, 'w', encoding='utf-8').write(css)
print("CSS written:", css.count('\n'), "lines")

# ── Fix notifications.js ────────────────────────────────────
notif = open(notif_path, encoding='utf-8').read()
print("Notif lines:", notif.count('\n'))
print("Has 2-tier:", 'riskScore >= 86' in notif)

if 'riskScore >= 86' not in notif:
    # Find the block by exact comment text
    targets = [
        '      // 5. High risk score',
        '      // 5.  High risk score',
        'High risk score'
    ]
    block_start = -1
    for t in targets:
        idx = notif.find(t)
        if idx >= 0:
            block_start = idx
            print(f"Found at index {idx}: {repr(notif[idx:idx+40])}")
            break

    if block_start < 0:
        print("Could not find risk block - searching for riskScore >= 65")
        idx = notif.find('riskScore >= 65')
        if idx >= 0:
            # Find start of this if block
            block_start = notif.rfind('\n', 0, idx) + 1
            print(f"Found riskScore >= 65 block at {block_start}")

    if block_start >= 0:
        # Find end: count braces from first {
        i = notif.find('{', block_start)
        depth = 0
        found_end = -1
        while i < len(notif):
            if notif[i] == '{': depth += 1
            elif notif[i] == '}':
                depth -= 1
                if depth == 0:
                    found_end = i + 1
                    break
            i += 1

        if found_end > 0:
            new_block = (
                '      // 5a. Critical risk score (86-100) - immediate escalation\n'
                '      if (tx.riskScore >= 86 && tx.riskStatus !== "ok") {\n'
                '        var keyCrit = tx.id + ":risk-crit";\n'
                '        if (!firedAlerts.has(keyCrit)) {\n'
                '          firedAlerts.add(keyCrit);\n'
                '          newAlerts.push(createNotification(tx.id, "risk-crit",\n'
                '            tx.id + " requires IMMEDIATE attention (Risk Score: " + tx.riskScore + "/100) - " + tx.currentStage\n'
                '          ));\n'
                '        }\n'
                '      }\n\n'
                '      // 5b. High risk score (70-85) - warning\n'
                '      if (tx.riskScore >= 70 && tx.riskScore < 86 && tx.riskStatus !== "ok") {\n'
                '        var keyWarn = tx.id + ":risk-warn";\n'
                '        if (!firedAlerts.has(keyWarn)) {\n'
                '          firedAlerts.add(keyWarn);\n'
                '          newAlerts.push(createNotification(tx.id, "risk-warn",\n'
                '            tx.id + " entered high-risk zone (Score: " + tx.riskScore + ") - " + tx.currentStage\n'
                '          ));\n'
                '        }\n'
                '      }'
            )
            notif = notif[:block_start] + new_block + notif[found_end:]
            print("Replaced risk block with 2-tier logic")
        else:
            print("ERROR: could not find block end brace")
    else:
        print("ERROR: could not locate high risk block at all")
        # Show lines 350-400 to debug
        lines = notif.split('\n')
        for i, l in enumerate(lines[350:410], 351):
            if 'risk' in l.lower() or 'score' in l.lower():
                print(f"  {i}: {l}")
else:
    print("Notif: 2-tier logic already present")

open(notif_path, 'w', encoding='utf-8').write(notif)
print("Notif written:", notif.count('\n'), "lines")
