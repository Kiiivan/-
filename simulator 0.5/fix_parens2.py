# Fix MARKER and APP_TAG - remove one extra ) at end
# 13 conditions means 13 ( and 13 )

MARKER = ('        struct_marker = " 🟢" if cat == "rural_china" else '
    '(" 🔴" if cat == "mechanical_solidarity" else '
    '(" 🔵" if cat == "organic_solidarity" else '
    '(" 🟣" if cat == "metropolis" else '
    '(" 🟪" if cat == "stranger_status" else '
    '(" 🟡" if cat == "risk_society" else '
    '(" ⚫" if cat == "rationalization" else '
    '(" ⚪" if cat == "disenchantment" else '
    '(" 🟠" if cat == "field_pressure_high" else '
    '(" 🟤" if cat == "cultural_capital_high" else '
    '(" ◑" if cat == "cultural_capital_low" else '
    '(" 🔶" if cat == "disciplinary_power" else '
    '(" 👁" if cat == "panopticism" else ""))))))))))))))')

APP_TAG = ('                    struct_tag = " 🟢" if cat == "rural_china" else '
    '(" 🔴" if cat == "mechanical_solidarity" else '
    '(" 🔵" if cat == "organic_solidarity" else '
    '(" 🟣" if cat == "metropolis" else '
    '(" 🟪" if cat == "stranger_status" else '
    '(" 🟡" if cat == "risk_society" else '
    '(" ⚫" if cat == "rationalization" else '
    '(" ⚪" if cat == "disenchantment" else '
    '(" 🟠" if cat == "field_pressure_high" else '
    '(" 🟤" if cat == "cultural_capital_high" else '
    '(" ◑" if cat == "cultural_capital_low" else '
    '(" 🔶" if cat == "disciplinary_power" else '
    '(" 👁" if cat == "panopticism" else ""))))))))))))))')

o1 = MARKER.count('(')
c1 = MARKER.count(')')
o2 = APP_TAG.count('(')
c2 = APP_TAG.count(')')
print(f'MARKER opens={o1} closes={c1} diff={o1-c1}')
print(f'APP_TAG opens={o2} closes={c2} diff={o2-c2}')

# Fix timeline.py
with open('modules/timeline.py', encoding='utf-8', errors='replace') as f:
    content = f.read()
lines = content.split('\n')
new_lines = []
changed = 0
for line in lines:
    if 'struct_marker = " 🟢"' in line and 'rural_china' in line:
        new_lines.append(MARKER)
        changed += 1
    elif 'struct_tag = " 🟢"' in line and 'rural_china' in line:
        new_lines.append(APP_TAG)
        changed += 1
    else:
        new_lines.append(line)
print(f'Changed {changed} lines')

new_content = '\n'.join(new_lines)
with open('modules/timeline.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

import ast
ast.parse(new_content)
print('timeline.py syntax OK')

# Fix app.py if needed
with open('app.py', encoding='utf-8', errors='replace') as f:
    app_content = f.read()
if 'struct_tag = " 🟢"' in app_content and 'rural_china' in app_content:
    app_lines = app_content.split('\n')
    app_new = []
    app_changed = 0
    for line in app_lines:
        if 'struct_tag = " 🟢"' in line and 'rural_china' in line:
            app_new.append(APP_TAG)
            app_changed += 1
        else:
            app_new.append(line)
    app_new_content = '\n'.join(app_new)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_new_content)
    ast.parse(app_new_content)
    print(f'app.py syntax OK ({app_changed} lines changed)')
else:
    print('app.py struct_tag already correct or different format')
