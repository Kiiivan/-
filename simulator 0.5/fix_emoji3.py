# Fix emoji markers in timeline.py and app.py
# Replace struct_marker/tag lines by finding and replacing the entire line

for fname in ['modules/timeline.py', 'app.py']:
    lines = open(fname, encoding='utf-8', errors='replace').read().split('\n')
    new_lines = []
    for line in lines:
        if line.strip().startswith('struct_marker = ') or line.strip().startswith('struct_tag = '):
            # Build correct 13-condition line
            if 'struct_marker' in line:
                new_lines.append('        struct_marker = " 🟢" if cat == "rural_china" else (" 🔴" if cat == "mechanical_solidarity" else (" 🔵" if cat == "organic_solidarity" else (" 🟣" if cat == "metropolis" else (" 🟪" if cat == "stranger_status" else (" 🟡" if cat == "risk_society" else (" ⚫" if cat == "rationalization" else (" ⚪" if cat == "disenchantment" else (" 🟠" if cat == "field_pressure_high" else (" 🟤" if cat == "cultural_capital_high" else (" ◑" if cat == "cultural_capital_low" else (" 🔶" if cat == "disciplinary_power" else (" 👁" if cat == "panopticism" else "")))))))))))))')
            else:
                new_lines.append('                    struct_tag = " 🟢" if cat == "rural_china" else (" 🔴" if cat == "mechanical_solidarity" else (" 🔵" if cat == "organic_solidarity" else (" 🟣" if cat == "metropolis" else (" 🟪" if cat == "stranger_status" else (" 🟡" if cat == "risk_society" else (" ⚫" if cat == "rationalization" else (" ⚪" if cat == "disenchantment" else (" 🟠" if cat == "field_pressure_high" else (" 🟤" if cat == "cultural_capital_high" else (" ◑" if cat == "cultural_capital_low" else (" 🔶" if cat == "disciplinary_power" else (" 👁" if cat == "panopticism" else "")))))))))))))')
        else:
            new_lines.append(line)
    open(fname, 'w', encoding='utf-8').write('\n'.join(new_lines))
    print(f'{fname} updated')

# Verify
import ast
ast.parse(open('modules/timeline.py', encoding='utf-8').read())
ast.parse(open('app.py', encoding='utf-8').read())
print('Syntax OK')
