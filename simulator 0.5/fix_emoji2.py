import re

# Fix timeline.py
with open('modules/timeline.py', 'rb') as f:
    content = f.read()

old = (
    b'struct_marker = " \xf0\x9f\x9f\xa2" if cat == "rural_china" else (" \xf0\x9f\x94\xb4" if cat == "mechanical_solidarity" else '
    b'(" \xf0\x9f\x95\xb5" if cat == "organic_solidarity" else (" \xf0\x9f\x9f\xa3" if cat == "metropolis" else '
    b'(" \xf0\x9f\x9f\xaa" if cat == "stranger_status" else (" \xf0\x9f\x9f\xa1" if cat == "risk_society" else '
    b'(" \xe2\x9a\xab" if cat == "rationalization" else (" \xe2\x9a\xaa" if cat == "disenchantment" else '
    b'(" \xf0\x9f\x9f\xa0" if cat == "field_pressure_high" else '
    b'(" \xf0\x9f\x9f\xa4" if cat == "cultural_capital_high" else '
    b'(" \xe2\x97\x91" if cat == "cultural_capital_low" else "")))))))))))'
)

new_marker = (
    b'struct_marker = " \xf0\x9f\x9f\xa2" if cat == "rural_china" else (" \xf0\x9f\x94\xb4" if cat == "mechanical_solidarity" else '
    b'(" \xf0\x9f\x95\xb5" if cat == "organic_solidarity" else (" \xf0\x9f\x9f\xa3" if cat == "metropolis" else '
    b'(" \xf0\x9f\x9f\xaa" if cat == "stranger_status" else (" \xf0\x9f\x9f\xa1" if cat == "risk_society" else '
    b'(" \xe2\x9a\xab" if cat == "rationalization" else (" \xe2\x9a\xaa" if cat == "disenchantment" else '
    b'(" \xf0\x9f\x9f\xa0" if cat == "field_pressure_high" else '
    b'(" \xf0\x9f\x9f\xa4" if cat == "cultural_capital_high" else '
    b'(" \xe2\x97\x91" if cat == "cultural_capital_low" else '
    b'(" \xf0\x9f\x94\xb6" if cat == "disciplinary_power" else '
    b'(" \xe2\x98\x9d" if cat == "panopticism" else "")))))))))))))'
)

if old in content:
    print('Found match in timeline.py, replacing...')
    content = content.replace(old, new_marker)
    with open('modules/timeline.py', 'wb') as f:
        f.write(content)
    print('timeline.py updated')
else:
    print('No match in timeline.py, trying simpler approach...')
    # Try without emoji bytes - just match the structure text
    # Find all struct_marker lines
    for i, line in enumerate(content.split(b'\n')):
        if b'struct_marker' in line:
            print(f'Line {i}: {line[:100]}')

# Fix app.py
with open('app.py', 'rb') as f:
    app_content = f.read()

old_app = (
    b'struct_tag = " \xf0\x9f\x9f\xa2" if cat == "rural_china" else (" \xf0\x9f\x94\xb4" if cat == "mechanical_solidarity" else '
    b'(" \xf0\x9f\x95\xb5" if cat == "organic_solidarity" else (" \xf0\x9f\x9f\xa3" if cat == "metropolis" else '
    b'(" \xf0\x9f\x9f\xaa" if cat == "stranger_status" else (" \xf0\x9f\x9f\xa1" if cat == "risk_society" else '
    b'(" \xe2\x9a\xab" if cat == "rationalization" else (" \xe2\x9a\xaa" if cat == "disenchantment" else '
    b'(" \xf0\x9f\x9f\xa0" if cat == "field_pressure_high" else '
    b'(" \xf0\x9f\x9f\xa4" if cat == "cultural_capital_high" else '
    b'(" \xe2\x97\x91" if cat == "cultural_capital_low" else "")))))))))))'
)

new_app_tag = (
    b'struct_tag = " \xf0\x9f\x9f\xa2" if cat == "rural_china" else (" \xf0\x9f\x94\xb4" if cat == "mechanical_solidarity" else '
    b'(" \xf0\x9f\x95\xb5" if cat == "organic_solidarity" else (" \xf0\x9f\x9f\xa3" if cat == "metropolis" else '
    b'(" \xf0\x9f\x9f\xaa" if cat == "stranger_status" else (" \xf0\x9f\x9f\xa1" if cat == "risk_society" else '
    b'(" \xe2\x9a\xab" if cat == "rationalization" else (" \xe2\x9a\xaa" if cat == "disenchantment" else '
    b'(" \xf0\x9f\x9f\xa0" if cat == "field_pressure_high" else '
    b'(" \xf0\x9f\x9f\xa4" if cat == "cultural_capital_high" else '
    b'(" \xe2\x97\x91" if cat == "cultural_capital_low" else '
    b'(" \xf0\x9f\x94\xb6" if cat == "disciplinary_power" else '
    b'(" \xe2\x98\x9d" if cat == "panopticism" else "")))))))))))))'
)

if old_app in app_content:
    print('Found match in app.py, replacing...')
    app_content = app_content.replace(old_app, new_app_tag)
    with open('app.py', 'wb') as f:
        f.write(app_content)
    print('app.py updated')
else:
    print('No match in app.py')

# Verify syntax
import ast
ast.parse(open('modules/timeline.py', encoding='utf-8').read())
ast.parse(open('app.py', encoding='utf-8').read())
print('Both files parse OK')
