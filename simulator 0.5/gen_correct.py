conditions = [
    ('rural_china', '🟢'),
    ('mechanical_solidarity', '🔴'),
    ('organic_solidarity', '🔵'),
    ('metropolis', '🟣'),
    ('stranger_status', '🟪'),
    ('risk_society', '🟡'),
    ('rationalization', '⚫'),
    ('disenchantment', '⚪'),
    ('field_pressure_high', '🟠'),
    ('cultural_capital_high', '🟤'),
    ('cultural_capital_low', '◑'),
    ('disciplinary_power', '🔶'),
    ('panopticism', '👁'),
]

indent_marker = '        '
indent_tag = '                    '

# Build the nested ternary expression
# Format: "emoji" if cat == "structure_id" else (...)
# For 13 conditions: opens=12, closes=12 at the end (after adding final else "")
# Wait: my concat produces: V0 if C0 else (V1 if C1 else (V2 if C2 else (...)))
# Each step adds: else (V_i if C_i else ) so each step adds 1 open and 0 closes
# At the final step: else "" + closes for all pending opens
# Total opens from else ( = N-1 = 12
# Total closes needed = N-1 = 12

# But my concatenation approach:
# step0: V0
# step1: V0 else (V1
# step2: V0 else (V1 else (V2
# ...
# step12 (final else ""): V0 else (V1 else (... else ("V12" if C12 else "")))

# So the string ends with: else "" + 12 closing )
# Number of ) = 12 (from the 12 nested else branches)

# Let's just build it programmatically
expr = f'"{conditions[0][1]}" if cat == "{conditions[0][0]}"'
for i in range(1, len(conditions)):
    expr = expr + f' else ("{conditions[i][1]}" if cat == "{conditions[i][0]}"'
# Add the final else and all the closing parens
expr = expr + ' else ""' + ')' * (len(conditions) - 1)

MARKER = indent_marker + expr
APP_TAG = indent_tag + expr

o = MARKER.count('(')
c = MARKER.count(')')
print(f'MARKER: opens={o} closes={c} diff={o-c}')

# Apply to timeline.py
with open('modules/timeline.py', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find and replace all struct_marker lines
lines = content.split('\n')
new_lines = []
for line in lines:
    if 'struct_marker = " 🟢"' in line and 'rural_china' in line:
        new_lines.append(MARKER)
        print('Replaced struct_marker line')
    elif 'struct_tag = " 🟢"' in line and 'rural_china' in line:
        new_lines.append(APP_TAG)
        print('Replaced struct_tag line')
    else:
        new_lines.append(line)

new_content = '\n'.join(new_lines)
with open('modules/timeline.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

# Apply to app.py
with open('app.py', encoding='utf-8', errors='replace') as f:
    app_content = f.read()
if 'struct_tag = " 🟢"' in app_content and 'rural_china' in app_content:
    app_lines = app_content.split('\n')
    app_new = []
    for line in app_lines:
        if 'struct_tag = " 🟢"' in line and 'rural_china' in line:
            app_new.append(APP_TAG)
            print('Replaced app.py struct_tag line')
        else:
            app_new.append(line)
    app_new_content = '\n'.join(app_new)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_new_content)

# Verify syntax
import ast
ast.parse(open('modules/timeline.py', encoding='utf-8').read())
print('timeline.py OK')
ast.parse(open('app.py', encoding='utf-8').read())
print('app.py OK')
print('ALL DONE')
