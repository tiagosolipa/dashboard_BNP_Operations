"""Fix CSS: update alert grid to 9 cols, add ops KPI/button styles"""

path = r'c:\Users\master\OneDrive - Universidade de Lisboa\DashboardBNP\styles.css'
with open(path, encoding='utf-8') as f:
    content = f.read()

# Update grid columns from 8 to 9
old_grid = 'grid-template-columns: 100px 180px 110px 110px 130px 110px 1fr 110px;'
new_grid = 'grid-template-columns: 80px 160px 100px 110px 120px 90px 1fr 80px 150px;'
content = content.replace(old_grid, new_grid)
print("Grid updated:", content.count(new_grid), "replacements")

# Append new ops styles at end
new_styles = """

/* ── OPS KPI GRID (2 rows x 4) ────────────────────────── */
.ops-kpi-row {
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 10px;
}

.ops-kpi {
  padding: 12px 14px;
}

.ops-kpi .kpi-value {
  font-size: 22px;
}

.icon-red-solid {
  background: var(--red);
  color: white;
}

.icon-amber {
  background: #fff8e1;
  color: #e65100;
}

/* ── PRIMARY SECTION (Alert Monitor) ──────────────────── */
.ops-primary-section {
  border-top: 3px solid var(--red);
  margin-bottom: 16px;
}

.ops-section-hint {
  font-size: 10px;
  color: var(--text-muted);
  margin-left: auto;
  font-style: italic;
}

/* ── ACTION BUTTONS IN ALERT TABLE ────────────────────── */
.al-action {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.ops-btn {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  border-radius: 4px;
  border: 1px solid;
  font-size: 10px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
  line-height: 1.3;
}

.ops-btn-review {
  background: var(--purple-light);
  color: var(--purple);
  border-color: var(--purple);
}
.ops-btn-review:hover { background: var(--purple); color: white; }

.ops-btn-resolve {
  background: var(--red-light);
  color: var(--red);
  border-color: var(--red);
}
.ops-btn-resolve:hover { background: var(--red); color: white; }

.ops-btn-approve {
  background: var(--green-light);
  color: var(--green);
  border-color: var(--green);
}
.ops-btn-approve:hover { background: var(--green); color: white; }

.ops-btn-advance {
  background: var(--blue-light);
  color: var(--blue);
  border-color: var(--blue);
  padding: 3px 7px;
}
.ops-btn-advance:hover { background: var(--blue); color: white; }

/* ── MODAL ACTION BUTTONS ──────────────────────────────── */
.modal-actions {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.modal-done {
  color: var(--bnp-green);
  font-weight: 700;
  font-size: 13px;
  padding: 8px 0;
}

.modal-ops-btn {
  padding: 9px 18px;
  border-radius: 6px;
  border: 1px solid;
  font-size: 12px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;
}

.modal-btn-review {
  background: var(--purple-light);
  color: var(--purple);
  border-color: var(--purple);
}
.modal-btn-review:hover { background: var(--purple); color: white; }

.modal-btn-approve {
  background: var(--green-light);
  color: var(--green);
  border-color: var(--green);
}
.modal-btn-approve:hover { background: var(--green); color: white; }

.modal-btn-resolve {
  background: var(--red-light);
  color: var(--red);
  border-color: var(--red);
}
.modal-btn-resolve:hover { background: var(--red); color: white; }

.modal-btn-advance {
  background: var(--blue-light);
  color: var(--blue);
  border-color: var(--blue);
}
.modal-btn-advance:hover { background: var(--blue); color: white; }

/* ── ALERTS STRIP: taller for action buttons ───────────── */
.alerts-strip {
  max-height: 520px;
}
"""

content += new_styles

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("CSS done")
