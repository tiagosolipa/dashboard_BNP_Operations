"""Fix notifications.js - tiered risk score notifications"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\master\OneDrive - Universidade de Lisboa\DashboardBNP\notifications.js'
with open(path, encoding='utf-8') as f:
    notif = f.read()

print(f"Read {len(notif)} chars, {notif.count(chr(10))} lines")

# Add two new alert type entries after existing high-risk entry
needle = '"high-risk":  { icon: '
if 'risk-warn' not in notif and needle in notif:
    idx = notif.find(needle)
    line_end = notif.find('\n', idx)
    insertion = (
        '\n    "risk-warn":  { icon: "\\u26a0",  label: "RISK WARNING",  color: "notif-orange", colorVar: "var(--orange)" },'
        '\n    "risk-crit":  { icon: "\\ud83d\\udd34", label: "RISK CRITICAL", color: "notif-red",    colorVar: "var(--red)" },'
    )
    notif = notif[:line_end] + insertion + notif[line_end:]
    print("Added alert types")

# Find the high-risk check block and replace with 2-tier
target = '      // 5. High risk score'
if target in notif and 'risk-crit' not in notif:
    s = notif.find(target)
    # find the matching closing brace
    depth = 0
    i = s
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
        notif = notif[:s] + new_block + notif[found_end:]
        print("Replaced with 2-tier logic")
    else:
        print("ERROR: could not find block end")
elif 'risk-crit' in notif:
    print("Already updated")

with open(path, 'w', encoding='utf-8') as f:
    f.write(notif)
print(f"Written: {notif.count(chr(10))} lines")
