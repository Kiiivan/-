MARKER = '        struct_marker = " 🟢" if cat == "rural_china" else (" 🔴" if cat == "mechanical_solidarity" else (" 🔵" if cat == "organic_solidarity" else (" 🟣" if cat == "metropolis" else (" 🟪" if cat == "stranger_status" else (" 🟡" if cat == "risk_society" else (" ⚫" if cat == "rationalization" else (" ⚪" if cat == "disenchantment" else (" 🟠" if cat == "field_pressure_high" else (" 🟤" if cat == "cultural_capital_high" else (" ◑" if cat == "cultural_capital_low" else (" 🔶" if cat == "disciplinary_power" else (" 👁" if cat == "panopticism" else "")))))))))))))'

opens = MARKER.count('(')
closes = MARKER.count(')')
print(f'opens={opens}, closes={closes}, diff={opens-closes}')

# Read timeline.py and count in the actual file
content = open('modules/timeline.py', encoding='utf-8', errors='replace').read()
line_found = None
for line in content.split('\n'):
    if 'struct_marker = " ' in line and 'rural_china' in line:
        line_found = line
        break

if line_found:
    o = line_found.count('(')
    c = line_found.count(')')
    print(f'File line: opens={o}, closes={c}, diff={o-c}')
    print(f'Line ends with: {repr(line_found[-50:])}')
else:
    print('No matching line found')
