"""补全三个新结构缺失事件的脚本"""
with open('data/events.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

# ---- cch: 在 cch_inherited_capital_crisis 之后插入 2 个事件 ----
cch_marker = '反思结构优势是可能的——但惯习仍会持续标记阶级出身（布迪厄）'
pos_cch = content.find(cch_marker)
if pos_cch < 0:
    print('ERROR: cch marker not found')
    exit(1)

cch_insert = '''
      - id: cch_objectified_capital_possession
        name: 客观化文化资本的占有
        age_range: [15, 40]
        weight: 0.4
        description: 「购买书籍、画作、乐器等文化商品——但消费需要身体化资本」
        outcomes:
          cultural_capital: [+0.1, +0.2]
          economic_capital: [-0.2, -0.3]
        sociological_reading: 「文化商品可以购买，但文化资本的消费需要预先灌输的时间和审美判断（布迪厄）」

      - id: cch_institutional_capital_defense
        name: 制度化资本的防御性维护
        age_range: [35, 60]
        weight: 0.35
        description: 「通过续约、评审委员、专业认证等维护已获得的制度化文化资本」
        outcomes:
          cultural_capital: [+0.1, +0.2]
          economic_capital: [-0.2, -0.3]
        sociological_reading: 「制度化资本需要持续维护，否则会因通胀或规则变化而贬值（布迪厄）」'''

# ---- ccl: 在 ccl_stability_in_necessity_taste 之后插入 2 个事件 ----
ccl_marker = '必然趣味在原阶级环境中有社交功能——适应而非反抗是低文化资本者的理性策略（布迪厄）'
pos_ccl = content.find(ccl_marker)
if pos_ccl < 0:
    print('ERROR: ccl marker not found')
    exit(1)

ccl_insert = '''
      - id: ccl_physical_decline_early
        name: 身体资本过早衰退
        age_range: [35, 50]
        weight: 0.45
        description: 「体能劳动者的身体在40岁后急剧衰退——唯一替代资本开始耗竭」
        outcomes:
          economic_capital: [-0.3, -0.4]
          stress_level: [+0.3, +0.5]
        sociological_reading: 「身体资本是不可逆的消耗品——一旦衰退，以身体资本为核心的替代路径就会崩塌（布迪厄）」

      - id: ccl_compensatory_morality
        name: 道德资本作为替代
        age_range: [20, 55]
        weight: 0.4
        description: 「通过勤劳、诚实、善良等道德品质获得社会认可——作为文化资本匮乏的补偿」
        outcomes:
          social_capital: [+0.2, +0.3]
          stress_level: [-0.1, -0.2]
        sociological_reading: 「道德资本是被统治阶级可用的替代性承认来源——但在符号市场上价值有限（布迪厄）」'''

# Find insertion point (after closing quote of the marker)
# The marker ends with ）」 - we insert right after it
end_cch = pos_cch + len(cch_marker)
content = content[:end_cch] + cch_insert + content[end_cch:]
print(f'Inserted cch events after byte {end_cch}')

# Re-find ccl marker (content may have shifted)
pos_ccl_new = content.find(ccl_marker)
end_ccl = pos_ccl_new + len(ccl_marker)
content = content[:end_ccl] + ccl_insert + content[end_ccl:]
print(f'Inserted ccl events after byte {end_ccl}')

with open('data/events.yaml', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
import yaml
f2 = open('data/events.yaml', 'r', encoding='utf-8')
data = yaml.safe_load(f2)
f2.close()
total = 0
for cat in ['field_pressure_high', 'cultural_capital_high', 'cultural_capital_low']:
    n = len(data['life_events'][cat].get('events', []))
    print(f'{cat}: {n} events')
    total += n
print(f'Total new events: {total}/66')