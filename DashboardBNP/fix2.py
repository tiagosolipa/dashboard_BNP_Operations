"""Fix 2: Add action cell to alert table rows and fix CSS grid"""
import re

path = r'c:\Users\master\OneDrive - Universidade de Lisboa\DashboardBNP\dashboard.js'
with open(path, encoding='utf-8') as f:
    content = f.read()

# Add action cell - find exact pattern
old = '            <span class="al-score-val">${tx.riskScore}</span>\n          </span>\n        </div>`;\n'
new = '            <span class="al-score-val">${tx.riskScore}</span>\n          </span>\n          <span class="al-action" onclick="event.stopPropagation()">${getActionBtn(tx)}</span>\n        </div>`;\n'

if old in content:
    content = content.replace(old, new)
    print("Added action cell to rows")
else:
    print("Pattern not found, trying alternate...")
    # Try with backtick
    idx = content.find('al-score-val')
    print(repr(content[idx-10:idx+120]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
