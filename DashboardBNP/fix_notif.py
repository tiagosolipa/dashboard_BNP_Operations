"""Fix notifications.js with tiered risk score notifications"""
path = r'c:\Users\master\OneDrive - Universidade de Lisboa\DashboardBNP\notifications.js'
with open(path, encoding='utf-8') as f:
    notif = f.read()

# Add two new alert types after the existing high-risk entry
old_type = '    "high-risk":  { icon: "\u26a0",  label: "HIGH RISK",     color: "notif-orange", colorVar: "var(--orange)" },'
new_type = ('    "high-risk":  { icon: "\u26a0",  label: "HIGH RISK",     color: "notif-orange", colorVar: "var(--orange)" },\n'
            '    "risk-warn":  { icon: "\u26a0",  label: "RISK WARNING",  color: "notif-orange", colorVar: "var(--orange)" },\n'
            '    "risk-crit":  { icon: "\ud83d\udd34", label: "RISK CRITICAL", color: "notif-red",    colorVar: "var(--red)" },')

if 'risk-warn' not in notif:
    notif = notif.replace(old_type, new_type)
    print("Added alert types")
else:
    print("Types already present")

# Find and replace the high-risk check
marker = '      // 5. High risk score'
if marker in notif and 'risk-crit' not in notif:
    # Find end of the block
    start = notif.find(marker)
    end = notif.find('    });', start) + len('    });') 
    old_block = notif[start:end]
    new_block = (
        '      // 5a. Critical risk score (86-100)\n'
        '      if (tx.riskScore >= 86 && tx.riskStatus !== "ok") {\n'
        '        var keyCrit = tx.id + ":risk-crit";\n'
        '        if (!firedAlerts.has(keyCrit)) {\n'
        '          firedAlerts.add(keyCrit);\n'
        '          newAlerts.push(createNotification(tx.id, "risk-crit",\n'
        '            tx.id + " requires IMMEDIATE attention (Risk Score: " + tx.riskScore + "/100) — " + tx.currentStage\n'
        '          ));\n'
        '        }\n'
        '      }\n\n'
        '      // 5b. High risk score (70-85)\n'
        '      if (tx.riskScore >= 70 && tx.riskScore < 86 && tx.riskStatus !== "ok") {\n'
        '        var keyWarn = tx.id + ":risk-warn";\n'
        '        if (!firedAlerts.has(keyWarn)) {\n'
        '          firedAlerts.add(keyWarn);\n'
        '          newAlerts.push(createNotification(tx.id, "risk-warn",\n'
        '            tx.id + " entered high-risk zone (Score: " + tx.riskScore + ") — " + tx.currentStage\n'
        '          ));\n'
        '        }\n'
        '      }\n'
        '    });'
    )
    notif = notif[:start] + new_block + notif[end:]
    print("Replaced high-risk check with 2-tier logic")
elif 'risk-crit' in notif:
    print("2-tier logic already present")
else:
    print("WARNING: could not find marker:", repr(notif[notif.find('5. High'):notif.find('5. High')+50]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(notif)
print("notifications.js done,", notif.count('\n'), "lines")
