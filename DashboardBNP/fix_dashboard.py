"""
Fix dashboard.js:
1. Remove orphaned chart function bodies (lines ~155 to risk popover)
2. Remove historicalChart function
3. Remove ApexCharts detail chart from openModal
4. Add action column to renderAlerts
5. Add modal action buttons to openModal
"""
import re

path = r'c:\Users\master\OneDrive - Universidade de Lisboa\DashboardBNP\dashboard.js'
with open(path, encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# ── 1. Find and remove orphaned chart code (between action handlers and risk popover) ──
# Find the line index of the risk popover comment
risk_pop_idx = None
for i, line in enumerate(lines):
    if '// \u2500\u2500 Risk Score Explanation Popover' in line:
        risk_pop_idx = i
        break

# Find where orphaned code starts (first non-empty line after getModalActions closing })
orphan_start = None
in_action_block = False
for i, line in enumerate(lines):
    if 'function getModalActions' in line:
        in_action_block = True
    if in_action_block and i > 150:
        if line.strip() == '}' and lines[i+1].strip() == '' if i+1 < len(lines) else False:
            # This is the closing } of getModalActions
            orphan_start = i + 1
            break

if orphan_start is None:
    # Fallback: find it by looking for orphaned 'const stages'
    for i, line in enumerate(lines):
        if i > 150 and 'const stages = [' in line and 'Capture' in line:
            orphan_start = i - 2
            break

print(f"Orphan start: {orphan_start}, Risk popover: {risk_pop_idx}")

if orphan_start is not None and risk_pop_idx is not None and orphan_start < risk_pop_idx:
    # Remove lines from orphan_start to risk_pop_idx (exclusive)
    lines = lines[:orphan_start] + [''] + lines[risk_pop_idx:]
    print(f"Removed orphaned chart code ({risk_pop_idx - orphan_start} lines)")

content = '\n'.join(lines)

# ── 2. Remove historicalChart function ──
hist_pattern = re.compile(
    r'\n// \u2500\u2500 Historical Daily Volume Chart.*?(?=\n// \u2500\u2500 Master Render)',
    re.DOTALL
)
content, n = re.subn(hist_pattern, '\n', content)
print(f"Removed historicalChart: {n} match(es)")

# ── 3. Remove ApexCharts detail chart from openModal ──
# Target: from "// Per-stage breakdown chart" to "detailChart.render();"
chart_in_modal = re.compile(
    r'\n\s*// Per-stage breakdown chart.*?detailChart\.render\(\);\n',
    re.DOTALL
)
content, n = re.subn(chart_in_modal, '\n', content)
print(f"Removed detail chart from openModal: {n} match(es)")

# Also remove: "if (detailChart) { detailChart.destroy()..." line if still present
content = re.sub(r'\s*if \(detailChart\) \{ detailChart\.destroy.*?\n', '\n', content)

# Remove the txDetailChart section header from modal if present
content = re.sub(r'\s*<div class="modal-section-title" style="margin-top:24px;">Time per Stage Breakdown</div>\n', '\n', content)
content = re.sub(r'\s*<div id="txDetailChart" style="height:200px; margin-top:8px;"></div>\n', '\n', content)

# ── 4. Add modal action buttons rendering in openModal ──
# Find where overlay.classList.add("open") is and insert getModalActions before it
if 'getModalActions' not in content or 'modalActions' not in content:
    content = content.replace(
        '  overlay.classList.add("open");\n  document.body.style.overflow = "hidden";\n}',
        '  const actEl = document.getElementById("modalActions");\n  if (actEl) actEl.innerHTML = getModalActions(tx);\n  overlay.classList.add("open");\n  document.body.style.overflow = "hidden";\n}'
    )
    print("Added modal action buttons")
else:
    print("Modal actions already wired")

# ── 5. Add Action column to renderAlerts table ──
# Update grid columns
old_grid = 'grid-template-columns: 100px 180px 110px 110px 130px 110px 1fr 110px;'
new_grid = 'grid-template-columns: 80px 160px 100px 110px 120px 90px 1fr 80px 150px;'

# Add the header span - find the risk-score-head span and add Action after it
old_header_end = '''        <span class="risk-score-head">
          Risk Score
          <button class="risk-info-btn" onclick="toggleRiskPopover(this)" title="How is this calculated?">&#9432;</button>
        </span>
      </div>'''
new_header_end = '''        <span class="risk-score-head">
          Risk Score
          <button class="risk-info-btn" onclick="toggleRiskPopover(this)" title="How is this calculated?">&#9432;</button>
        </span>
        <span>Action</span>
      </div>'''

if old_header_end in content:
    content = content.replace(old_header_end, new_header_end)
    print("Added Action header column")
else:
    print("WARNING: Could not find alert table header")

# Add action cell to row - find the closing score cell and add action after
old_row_end = '''          <span class="al-score-cell">
            <div class="al-score-bar-wrap">
              <div class="al-score-bar" style="width:${scoreWidth}%;background:${tx.priority === 'high' ? '#e53935' : tx.priority === 'medium' ? '#f5a623' : '#1976d2'};"></div>
            </div>
            <span class="al-score-val">${tx.riskScore}</span>
          </span>
        </div>\`;'''
new_row_end = '''          <span class="al-score-cell">
            <div class="al-score-bar-wrap">
              <div class="al-score-bar" style="width:${scoreWidth}%;background:${tx.priority === 'high' ? '#e53935' : tx.priority === 'medium' ? '#f5a623' : '#1976d2'};"></div>
            </div>
            <span class="al-score-val">${tx.riskScore}</span>
          </span>
          <span class="al-action" onclick="event.stopPropagation()">${getActionBtn(tx)}</span>
        </div>\`;'''

if old_row_end in content:
    content = content.replace(old_row_end, new_row_end)
    print("Added action cell to alert rows")
else:
    print("WARNING: Could not find alert row end pattern")

# ── Write back ──
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Lines:", content.count('\n'))
