# Read timeline.py, find the 3 struct_marker lines, and replace them with correct 13-condition lines

MARKER = '        struct_marker = " 🟢" if cat == "rural_china" else (" 🔴" if cat == "mechanical_solidarity" else (" 🔵" if cat == "organic_solidarity" else (" 🟣" if cat == "metropolis" else (" 🟪" if cat == "stranger_status" else (" 🟡" if cat == "risk_society" else (" ⚫" if cat == "rationalization" else (" ⚪" if cat == "disenchantment" else (" 🟠" if cat == "field_pressure_high" else (" 🟤" if cat == "cultural_capital_high" else (" ◑" if cat == "cultural_capital_low" else (" 🔶" if cat == "disciplinary_power" else (" 👁" if cat == "panopticism" else "")))))))))))))'

with open('modules/timeline.py', encoding='utf-8', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
for line in lines:
    if line.strip().startswith('struct_marker = "'):
        new_lines.append(MARKER)
    else:
        new_lines.append(line)

new_content = '\n'.join(new_lines)
with open('modules/timeline.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

# Verify
import ast
ast.parse(new_content)
print('timeline.py syntax OK')

# Fix app.py struct_tag if needed
with open('app.py', encoding='utf-8', errors='replace') as f:
    app_content = f.read()

if 'struct_tag = " 🟢"' in app_content:
    APP_TAG = '                    struct_tag = " 🟢" if cat == "rural_china" else (" 🔴" if cat == "mechanical_solidarity" else (" 🔵" if cat == "organic_solidarity" else (" 🟣" if cat == "metropolis" else (" 🟪" if cat == "stranger_status" else (" 🟡" if cat == "risk_society" else (" ⚫" if cat == "rationalization" else (" ⚪" if cat == "disenchantment" else (" 🟠" if cat == "field_pressure_high" else (" 🟤" if cat == "cultural_capital_high" else (" ◑" if cat == "cultural_capital_low" else (" 🔶" if cat == "disciplinary_power" else (" 👁" if cat == "panopticism" else "")))))))))))))'

    app_lines = app_content.split('\n')
    app_new = []
    for line in app_lines:
        if line.strip().startswith('struct_tag = " 🟢"'):
            app_new.append(APP_TAG)
        else:
            app_new.append(line)
    app_new_content = '\n'.join(app_new)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_new_content)
    ast.parse(app_new_content)
    print('app.py syntax OK')
else:
    print('app.py already fixed or no struct_tag found')
