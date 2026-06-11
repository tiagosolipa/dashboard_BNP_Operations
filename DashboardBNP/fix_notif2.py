"""Fix notifications.js - safe read/modify/write with encoding check"""
import codecs

path = r'c:\Users\master\OneDrive - Universidade de Lisboa\DashboardBNP\notifications.js'

# Read with explicit encoding detection
with codecs.open(path, 'r', encoding='utf-8-sig') as f:
    notif = f.read()

print(f"Read {len(notif)} chars, {notif.count(chr(10))} lines")

# Add two new alert type entries after existing high-risk entry
old_type = '    "high-risk":  { icon: "\u26a0",  label: "HIGH RISK",     color: "notif-orange", colorVar: "var(--orange)" },'
new_types_addition = (
    '\n    "risk-warn":  { icon: "\u26a0",  label: "RISK WARNING",  color: "notif-orange", colorVar: "var(--orange)" },'
    '\n    "risk-crit":  { icon: "\ud83d\udd34", label: "RISK CRITICAL", color: "notif-red",    colorVar: "var(--red)" },'
)

if old_type in notif and 'risk-warn' not in notif:
    notif = notif.replace(old_type, old_type + new_types_addition)
    print("Added risk-warn and risk-crit alert types")
else:
    print("Types check:", 'risk-warn' in notif, old_type in notif)

# Replace the single high-risk check block with 2-tier logic
# Find the exact text block to replace
target_start = '      // 5. High risk score'
if target_start in notif:
    s = notif.find(target_start)
    # Find the closing }); of this block
    # The block structure is: if(...){ var keyRisk...; if(!has){ add; push; } } }
    # Find end by counting braces from start
    depth = 0
    found_end = -1
    i = notif.find('{', s)
    while i < len(notif):
        if notif[i] == '{':
            depth += 1
        elif notif[i] == '}':
            depth -= 1
            if depth == 0:
                found_end = i + 1
                break
        i += 1
    if found_end > 0:
        old_block = notif[s:found_end]
        print(f"Found block ({len(old_block)} chars): {repr(old_block[:60])}")
        new_block = (
            '      // 5a. Critical risk score (86-100) — immediate escalation\n'
            '      if (tx.riskScore >= 86 && tx.riskStatus !== "ok") {\n'
            '        var keyCrit = tx.id + ":risk-crit";\n'
            '        if (!firedAlerts.has(keyCrit)) {\n'
            '          firedAlerts.add(keyCrit);\n'
            '          newAlerts.push(createNotification(tx.id, "risk-crit",\n'
            '            tx.id + " requires IMMEDIATE attention (Risk Score: " + tx.riskScore + "/100) — " + tx.currentStage\n'
            '          ));\n'
            '        }\n'
            '      }\n\n'
            '      // 5b. High risk score (70-85) — warning\n'
            '      if (tx.riskScore >= 70 && tx.riskScore < 86 && tx.riskStatus !== "ok") {\n'
            '        var keyWarn = tx.id + ":risk-warn";\n'
            '        if (!firedAlerts.has(keyWarn)) {\n'
            '          firedAlerts.add(keyWarn);\n'
            '          newAlerts.push(createNotification(tx.id, "risk-warn",\n'
            '            tx.id + " entered high-risk zone (Score: " + tx.riskScore + ") — " + tx.currentStage\n'
            '          ));\n'
            '        }\n'
            '      }'
        )
        notif = notif[:s] + new_block + notif[found_end:]
        print("Replaced high-risk block with 2-tier logic")
    else:
        print("Could not find block end")
else:
    print("Could not find target:", target_start[:30])

# Encode check - make sure output is valid utf-8
try:
    encoded = notif.encode('utf-8')
    print(f"Encoding OK: {len(encoded)} bytes")
except UnicodeEncodeError as e:
    print(f"Encode error: {e}")
    # Find problem chars
    for i, c in enumerate(notif):
        try: c.encode('utf-8')
        except: print(f"  Bad char at {i}: {repr(c)}")

with codecs.open(path, 'w', encoding='utf-8') as f:
    f.write(notif)
print(f"Written: {notif.count(chr(10))} lines")
