content = open('modules/timeline.py', encoding='utf-8').read()

old = 'struct_marker = " 🟢" if cat == "rural_china" else (" 🔴" if cat == "mechanical_solidarity" else (" 🔵" if cat == "organic_solidarity" else (" 🟣" if cat == "metropolis" else (" 🟪" if cat == "stranger_status" else (" 🟡" if cat == "risk_society" else (" ⚫" if cat == "rationalization" else (" ⚪" if cat == "disenchantment" else (" 🟠" if cat == "field_pressure_high" else (" 🟤" if cat == "cultural_capital_high" else (" ◑" if cat == "cultural_capital_low" else "")))))))))))'

new = 'struct_marker = " 🟢" if cat == "rural_china" else (" 🔴" if cat == "mechanical_solidarity" else (" 🔵" if cat == "organic_solidarity" else (" 🟣" if cat == "metropolis" else (" 🟪" if cat == "stranger_status" else (" 🟡" if cat == "risk_society" else (" ⚫" if cat == "rationalization" else (" ⚪" if cat == "disenchantment" else (" 🟠" if cat == "field_pressure_high" else (" 🟤" if cat == "cultural_capital_high" else (" ◑" if cat == "cultural_capital_low" else (" 🔶" if cat == "disciplinary_power" else (" 👁" if cat == "panopticism" else ""))))))))))))))'

# Verify counts
oc = old.count('(')
cc = old.count(')')
print(f'OLD: opens={oc}, closes={cc}, diff={oc-cc}')
oc2 = new.count('(')
cc2 = new.count(')')
print(f'NEW: opens={oc2}, closes={cc2}, diff={oc2-cc2}')

new_content = content.replace(old, new)
changed = new_content != content
print(f'Changed: {changed}, occurrences replaced: {content.count(old)}')

open('modules/timeline.py', 'w', encoding='utf-8').write(new_content)
print('Done')
