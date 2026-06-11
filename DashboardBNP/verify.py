import sys
sys.stdout.reconfigure(encoding='utf-8')
js = open('dashboard.js', encoding='utf-8').read()
html = open('index.html', encoding='utf-8').read()
notif = open('notifications.js', encoding='utf-8').read()
css = open('styles.css', encoding='utf-8').read()
checks = [
    ('JS: renderStageErrors function', 'function renderStageErrors' in js),
    ('JS: filterByStageErr function', 'function filterByStageErr' in js),
    ('JS: riskScoreFilter in state', 'riskScoreFilter: null' in js),
    ('JS: riskScoreFilter in renderAlerts', 'state.riskScoreFilter' in js),
    ('JS: renderStageErrors in render()', 'renderStageErrors(filtered)' in js),
    ('JS: riskScoreFilterBar listener', 'riskScoreFilterBar' in js),
    ('JS: performAction', 'function performAction' in js),
    ('JS: getActionBtn', 'function getActionBtn' in js),
    ('JS: getModalActions', 'function getModalActions' in js),
    ('JS: getMonth+1 fix', 'getMonth() + 1' in js),
    ('HTML: stageErrorsPanel', 'stageErrorsPanel' in html),
    ('HTML: riskScoreFilterBar', 'riskScoreFilterBar' in html),
    ('HTML: rs-chip buttons (5+)', html.count('rs-chip') >= 5),
    ('HTML: 8 ops-kpi cards', html.count('ops-kpi') >= 8),
    ('CSS: stage-errors-panel', 'stage-errors-panel' in css),
    ('CSS: rs-chip', 'rs-chip' in css),
    ('CSS: ops-btn', 'ops-btn' in css),
    ('CSS: modal-actions', 'modal-actions' in css),
    ('Notif: risk-warn type', 'risk-warn' in notif),
    ('Notif: risk-crit type', 'risk-crit' in notif),
    ('Notif: 2-tier 86+', 'riskScore >= 86' in notif),
    ('Notif: 2-tier 70-86', 'riskScore >= 70' in notif),
]
fails = 0
for lbl, ok in checks:
    print(('[OK]  ' if ok else '[FAIL]') + ' ' + lbl)
    if not ok: fails += 1
print()
print('Result: {}/{} checks passed'.format(len(checks)-fails, len(checks)))
