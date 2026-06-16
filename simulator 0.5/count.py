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

print(f'Total chars: {len(MARKER)}')
print(f'Opens: {MARKER.count("("}, Closes: {MARKER.count(")")}')

# Find the structure
# The key is: each condition is: if cat == X else ( ... )
# So if there are 13 conditions, there are 12 ( because condition1 is if (no open) and condition2-13 are elif (each has an open)
# But wait - the structure is:
# A if cond else B
# where A itself is: C if cond2 else D
# etc.
# Each ( starts a new level, each ) ends a level
# So: if cond1 else (if cond2 else (if cond3 ... else (if cond13 else ""))))

# Let me count the actual emoji+condition groups:
import re
conditions = re.findall(r'\("[^"]+" if cat', MARKER)
print(f'Condition groups (excl last else): {len(conditions)}')

# Count all ( and ) by position
opens = []
closes = []
for i, ch in enumerate(MARKER):
    if ch == '(':
        opens.append(i)
    elif ch == ')':
        closes.append(i)

print(f'Total opens: {len(opens)}, Total closes: {len(closes)}')
print(f'Opens at: {opens}')
print(f'Closes at: {closes}')
print(f'MARKER ends with: {repr(MARKER[-50:])}')
