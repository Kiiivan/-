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

indent = '        '
parts = []
for i, (cat, emoji) in enumerate(conditions):
    if i == 0:
        parts.append(f'"{emoji}" if cat == "{cat}"')
    else:
        parts.append(f'("{emoji}" if cat == "{cat}"')

# Build nested structure
# For N conditions: A if c1 else (B if c2 else (C if c3 else (...Z else "")))
# Each ) after an inner if closes one nesting level
# We need N-1 closing ) at the end for the N-1 inner branches
# Plus the outermost closing ) for the value expression

# Build it:
# cond0 if cat0 else (cond1 if cat1 else (cond2 if cat2 else (... )))

# String construction:
inner = parts[0]
for p in parts[1:]:
    inner = inner + ' if cat else (' + p

# Actually that's wrong. Let me do it properly:
# tier0 value if cond0 else (tier1 value if cond1 else (tier2 value if cond2 ... else tierN))
# tier0 = emoji0 if cat0
# tier1 = emoji1 if cat1
# etc.
# So the nested expression is:
# A if cond0 else (B if cond1 else (C if cond2 else (...Z if condN)))

# For 13 conditions:
# tier0 if cond0 else (tier1 if cond1 else (tier2 if cond2 else (...)))

# tier0 = emoji0 if cat0
# tier1 = emoji1 if cat1
# ...
# tier12 = emoji12 if cat12

# The string:
line = indent + parts[0] + ' if cat == "' + conditions[0][0] + '" else (' + parts[1] + ' if cat == "' + conditions[1][0] + '" else (' + parts[2] + ' if cat == "' + conditions[2][0] + '" else (' + parts[3] + ' if cat == "' + conditions[3][0] + '" else (' + parts[4] + ' if cat == "' + conditions[4][0] + '" else (' + parts[5] + ' if cat == "' + conditions[5][0] + '" else (' + parts[6] + ' if cat == "' + conditions[6][0] + '" else (' + parts[7] + ' if cat == "' + conditions[7][0] + '" else (' + parts[8] + ' if cat == "' + conditions[8][0] + '" else (' + parts[9] + ' if cat == "' + conditions[9][0] + '" else (' + parts[10] + ' if cat == "' + conditions[10][0] + '" else (' + parts[11] + ' if cat == "' + conditions[11][0] + '" else "")))))

# Let's simplify: build the string programmatically
strs = []
for i, (cat, emoji) in enumerate(conditions):
    strs.append(f'"{emoji}" if cat == "{cat}"')

# Now nest them
result = strs[0]
for s in strs[1:]:
    result = result + ' else (' + s
result = result + ' else ""' + ')' * (len(strs) - 1)

print(f'Number of conditions: {len(conditions)}')
print(f'Opening parens in inner loops: {len(conditions)-1}')
print(f'Closing parens at end: {len(conditions)-1}')
line = indent + result

# Verify
opens = line.count('(')
closes = line.count(')')
print(f'opens={opens}, closes={closes}, diff={opens-closes}')

# Show start and end
print('START:', line[:100])
print('END:', line[-100:])
