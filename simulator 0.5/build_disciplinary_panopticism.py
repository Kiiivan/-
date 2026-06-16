"""安全追加 disciplinary_power 和 panopticism 事件库到 events.yaml"""
with open('data/events.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

# ============ disciplinary_power 事件库（22个）============

disciplinary_power_events = '''
  # ============================================================
  # 【规训社会事件】- 22个（福柯《规训与惩罚》体系）
  # ============================================================
  disciplinary_power:
    description: 规训社会特有事件——驯顺肉体、时间纪律、层级监视、规范化裁决、检查制度
    events:
      - id: dp_time_table_tyranny
        name: 时间表的暴政
        age_range: [6, 12]
        weight: 0.65
        description: 「从家庭弹性时间进入学校时间表——起床、进食、学习、排泄全部被精确规定」
        outcomes:
          time_discipline: [+0.4, +0.5]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「规训从对时间的精确控制开始——修道院时间制度被移植到学校（福柯）」

      - id: dp_spatial_cell_allocation
        name: 固定座位分配
        age_range: [6, 15]
        weight: 0.55
        description: 「被分配到教室固定座位——位置按成绩、身高、视力排列，空间即等级标记」
        outcomes:
          spatial_mobility: [-0.2, -0.3]
          conformity_tendency: [+0.2, +0.3]
        sociological_reading: 「空间分配是规训的基础技术——每个人有自己的位置，每个位置有确定的人（福柯）」

      - id: dp_first_ranking
        name: 第一次考试排名
        age_range: [7, 10]
        weight: 0.7
        description: 「首次发现自己被置于可比序列中——从此知道自己是第X名」
        outcomes:
          normalizing_judgment: [+0.3, +0.4]
          stress_level: [+0.2, +0.4]
        sociological_reading: 「检查制造了可见的可排序个体——个体从被教育对象变成可被比较的案例（福柯）」

      - id: dp_posture_correction
        name: 姿势矫正
        age_range: [7, 12]
        weight: 0.5
        description: 「被纠正坐姿、握笔方式、排队方式——身体被规训为正确形态」
        outcomes:
          body_control: [+0.3, +0.4]
          stress_level: [+0.1, +0.2]
        sociological_reading: 「规训对身体进行精细操作——驯顺的肉体是规训的首要产品（福柯）」

      - id: dp_examination_frequency
        name: 考试密度升级
        age_range: [12, 18]
        weight: 0.7
        description: 「初高中阶段考试频率急剧增加——单元测、月考、期中考、期末考轮番轰炸」
        outcomes:
          examination_frequency: [+0.4, +0.5]
          stress_level: [+0.3, +0.4]
        sociological_reading: 「检查是规训的核心技术——考试将学生不断转化为可被记录和评判的案例（福柯）」

      - id: dp_tracking_assignment
        name: 中考分流——轨道分配
        age_range: [14, 16]
        weight: 0.75
        description: 「第一次制度性分流——普高、职高、辍学。轨道一旦确定难以转换」
        outcomes:
          spatial_allocation: [+0.3, +0.4]
          stress_level: [+0.3, +0.5]
        sociological_reading: 「分流是规范化裁决的制度化——将个体分配到预先确定的能力序列中（福柯）」

      - id: dp_hierarchical_surveillance
        name: 层级监视的强化
        age_range: [12, 18]
        weight: 0.65
        description: 「班主任后窗观察、监控摄像头、手机管控——监视无处不在且持续」
        outcomes:
          surveillance_intensity: [+0.4, +0.5]
          internalized_surveillance: [+0.2, +0.3]
        sociological_reading: 「层级监视是规训建筑学的核心——监视者本身也被监视，形成无限递归（福柯）」

      - id: dp_body_standardization
        name: 身体标准化
        age_range: [12, 18]
        weight: 0.55
        description: 「校服规定、发型规定、男女间距规定——身体的一切外在表现都被标准化」
        outcomes:
          body_control: [+0.3, +0.4]
          conformity_tendency: [+0.2, +0.3]
        sociological_reading: 「规训对身体进行标准化——制造驯顺而可被精确操纵的肉体（福柯）」

      - id: dp_kpi_system_entry
        name: KPI绩效考核系统
        age_range: [22, 30]
        weight: 0.65
        description: 「被纳入绩效考核体系——工作的一切方面都被量化、排名、比较」
        outcomes:
          normalizing_judgment: [+0.3, +0.5]
          time_discipline: [+0.2, +0.3]
        sociological_reading: 「工厂规训无缝迁移到职场——时间表暴政变成KPI暴政（福柯）」

      - id: dp_time_clock_obedience
        name: 打卡制度与考勤纪律
        age_range: [22, 40]
        weight: 0.6
        description: 「每天打卡、迟到扣款、加班无补——时间纪律从学校延续到职场」
        outcomes:
          time_discipline: [+0.3, +0.4]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「打卡制度是规训时间控制的技术延伸——使肉体被精确嵌入时间网格（福柯）」

      - id: dp_management_position_split
        name: 管理岗与被管理岗分化
        age_range: [28, 40]
        weight: 0.5
        description: 「成为监视者或继续被监视——监视者本身也被更上层监视」
        outcomes:
          authority_orientation: [+0.2, +0.4]
          surveillance_intensity: [+0.2, +0.3]
        sociological_reading: 「层级监视是递归的——下级监视个体，中级监视下级，上级监视中级（福柯）」

      - id: dp_mortgage_discipline_lock
        name: 房贷纪律锁定
        age_range: [28, 40]
        weight: 0.55
        description: 「房贷将时间纪律永久化——不敢迟到、不敢辞职、不敢偏离」
        outcomes:
          time_discipline: [+0.3, +0.4]
          spatial_mobility: [-0.3, -0.4]
        sociological_reading: 「经济规训与制度规训合流——物质债务变成时间纪律的永久枷锁（福柯）」

      - id: dp_health_check_institution
        name: 年度体检制度化
        age_range: [30, 50]
        weight: 0.5
        description: 「检查制度延伸到身体内部——每一次体检都是一次规范化裁决」
        outcomes:
          examination_frequency: [+0.2, +0.3]
          stress_level: [+0.1, +0.2]
        sociological_reading: 「检查同时是监视与裁决——医疗检查变成道德健康与否的判断（福柯）」

      - id: dp_intergenerational_discipline_transfer
        name: 规训的代际传递
        age_range: [28, 45]
        weight: 0.55
        description: 「将自身内化的规训传递给下一代——督促学习、纠正姿势、规划时间表」
        outcomes:
          conformity_tendency: [+0.1, +0.2]
          stress_level: [+0.1, +0.2]
        sociological_reading: 「规训通过家庭实现代际再生产——父母成为规训系统的基层执行者（福柯）」

      - id: dp_minor_punishment_system
        name: 微观惩罚系统
        age_range: [6, 30]
        weight: 0.6
        description: 「迟到罚款、注意力不集中被告状、姿势不正被矫正——规训的微观惩罚无处不在」
        outcomes:
          normalization_pressure: [+0.3, +0.4]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「规训存在一个微型司法系统——惩罚一切偏离规范的行为（福柯）」

      - id: dp_progression_sequence
        name: 序列进阶考核
        age_range: [18, 30]
        weight: 0.55
        description: 「从简单到复杂、从易到难的渐进程序——每个阶段是前一阶段的条件」
        outcomes:
          merit_accumulation: [+0.2, +0.3]
          time_discipline: [+0.1, +0.2]
        sociological_reading: 「规训用序列替代平等——操练使肉体逐步适应更复杂的任务（福柯)"

      - id: dp_confinement_threat
        name: 禁闭威胁
        age_range: [10, 25]
        weight: 0.45
        description: 「威胁送工读学校、少管所——禁闭的可能性本身就是规训工具」
        outcomes:
          normalization_pressure: [+0.3, +0.4]
          stress_level: [+0.2, +0.4]
        sociological_reading: 「禁闭是规训的极端形式——威胁本身比实际禁闭更能生产顺从（福柯）」

      - id: dp_worker_discipline_transfer
        name: 从学校规训到工厂规训
        age_range: [16, 22]
        weight: 0.5
        description: 「从学校时间表转到工厂流水线——学术规训无缝转换为劳动规训」
        outcomes:
          time_discipline: [+0.2, +0.3]
          body_control: [+0.2, +0.3]
        sociological_reading: 「规训技术在制度间互相借用——学校成为工厂的预备阶段（福柯）」

      - id: dp_collective_drill
        name: 集体操练
        age_range: [16, 25]
        weight: 0.45
        description: 「军训、团体操、集体跑操——多个身体在时间和空间上被协调配合」
        outcomes:
          collective_coordination: [+0.3, +0.4]
          conformity_tendency: [+0.2, +0.3]
        sociological_reading: 「规训将单个肉体组合为集体力量——使分散的身体产生协调的效力（福柯）」

      - id: dp_documentation_case
        name: 档案化——从人到案例
        age_range: [6, 35]
        weight: 0.55
        description: 「成绩单、处分记录、考核档案——个体被持续书写、记录、归档」
        outcomes:
          documentation_intensity: [+0.3, +0.4]
          stress_level: [+0.1, +0.2]
        sociological_reading: 「检查使书写成为权力工具——被书写者失去对自身叙事的控制（福柯）」

      - id: dp_interrogation_audit
        name: 审计与盘问
        age_range: [25, 50]
        weight: 0.5
        description: 「内部审计、工作汇报、述职报告——每一个人都可能被随时盘问」
        outcomes:
          surveillance_intensity: [+0.3, +0.4]
          stress_level: [+0.2, +0.4]
        sociological_reading: 「盘问是规训权力的核心仪式——检查者与被检查者的权力不对称被反复再生产（福柯）」

      - id: dp_retirement_discipline_legacy
        name: 退休后规训遗迹
        age_range: [55, 70]
        weight: 0.4
        description: 「从时间表暴政中解放，但数十年规训已形成身体记忆——仍然按时起床、按部就班」
        outcomes:
          time_discipline: [-0.1, +0.1]
          stress_level: [-0.2, -0.1]
        sociological_reading: 「规训的身体记忆难以消除——退休不是解放而是规训的慢性化（福柯）」

'''

# ============ panopticism 事件库（22个）============

panopticism_events = '''
  # ============================================================
  # 【全景敞视事件】- 22个（福柯《规训与惩罚》《临床医学的诞生》体系）
  # ============================================================
  panopticism:
    description: 全景敞视特有事件——可见性陷阱、权力自动化、内化监视、永恒审判、数字透明
    events:
      - id: pan_imaginary_audience
        name: 假想观众心理的形成
        age_range: [4, 8]
        weight: 0.6
        description: 「从幼年就发展出假想观众——每做一个决定都假设有人在观察」
        outcomes:
          internalized_surveillance: [+0.4, +0.5]
          spontaneity: [-0.2, -0.3]
        sociological_reading: 「一种虚构的关系生产出一种真实的服从——假想观众是全景敞视的内化形式（福柯）」

      - id: pan_shame_education
        name: 耻感教育
        age_range: [4, 10]
        weight: 0.6
        description: 「犯错时不是被告知这是错的，而是被别人看到会怎样——羞耻感替代体罚」
        outcomes:
          shame_sensitivity: [+0.3, +0.4]
          self_monitoring: [+0.3, +0.4]
        sociological_reading: 「耻感教育是全景敞视的温和形式——使权力效应在无监视者的情况下持续生效（福柯）」

      - id: pan_visibility_trap
        name: 可见性陷阱启动
        age_range: [12, 20]
        weight: 0.65
        description: 「社交媒体时代——假想观众变成真实观众，每条动态都是一次检查和裁决」
        outcomes:
          visibility_trap: [+0.4, +0.5]
          self_censorship: [+0.3, +0.5]
        sociological_reading: 「数字技术使全景敞视达到极致——每一个行为都被永久记录和可见化（福柯）」

      - id: pan_social_media_audit
        name: 社交媒体审计
        age_range: [13, 25]
        weight: 0.55
        description: 「发帖前的犹豫、删帖的冲动、对评论的焦虑——全景敞视在数字空间完美实现」
        outcomes:
          self_censorship: [+0.3, +0.4]
          stress_level: [+0.2, +0.4]
        sociological_reading: 「社交媒体是数字全景敞视——可见性陷阱在虚拟空间中无限放大（福柯）」

      - id: pan_credit_score_system
        name: 信用评分体系进入
        age_range: [18, 30]
        weight: 0.6
        description: 「每一次还款、每一次违约、每一次申请都影响信用分——算法裁决代替人工判断」
        outcomes:
          algorithmic_judgment: [+0.3, +0.4]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「信用评分是全景敞视的算法形式——每一个数字痕迹都是一次检查（福柯）」

      - id: pan_internalized_surveillance_deep
        name: 内化监视的深度内化
        age_range: [25, 45]
        weight: 0.6
        description: 「不需要外部催促就主动加班、主动汇报、主动检查——成为自我规训的典范」
        outcomes:
          internalized_surveillance: [+0.4, +0.5]
          spontaneity: [-0.3, -0.4]
        sociological_reading: 「全景敞视的终极产物是不需要看守的囚徒——权力效应在无行使者的情况下自动运转（福柯）」

      - id: pan_performative_self
        name: 表演性自我呈现
        age_range: [18, 40]
        weight: 0.55
        description: 「即使在私密空间中也难以放松——表演性的自我呈现已深入骨髓」
        outcomes:
          spontaneity: [-0.3, -0.4]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「全景敞视使内在性消失——自我变成可被观察和评判的表演（福柯）」

      - id: pan_algorithmic_employment
        name: 算法就业筛选
        age_range: [20, 30]
        weight: 0.55
        description: 「简历被AI筛选——年龄、性别、学历、社交媒体——算法裁决代替人的判断」
        outcomes:
          data_footprint: [+0.3, +0.4]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「算法是全景敞视的建筑师——以最少的可见性实现最大的权力效应（福柯）」

      - id: pan_digital_tattoo
        name: 数字纹身的永久性
        age_range: [18, 40]
        weight: 0.5
        description: 「年轻时的每一次网络行为都可能被永久记录——数字空间没有遗忘」
        outcomes:
          data_footprint: [+0.3, +0.4]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「数字纹身是全景敞视的终极形态——检查制度的永久化（福柯）」

      - id: pan_visibility_anxiety
        name: 可见性焦虑
        age_range: [13, 35]
        weight: 0.55
        description: 「被记录、被追踪、被评分——在数字全景敞视中时刻感到被凝视的焦虑」
        outcomes:
          internalized_surveillance: [+0.3, +0.4]
          stress_level: [+0.3, +0.5]
        sociological_reading: 「可见性是双刃剑——凝视他者的同时也被他者凝视，全景敞视使这种不对称永久化（福柯）」

      - id: pan_self_censorship_internet
        name: 网络自我审查
        age_range: [13, 30]
        weight: 0.6
        description: 「发帖前的犹豫、评论时的自我审查——知道一切皆可被追溯」
        outcomes:
          self_censorship: [+0.4, +0.5]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「自我审查是内化监视的日常表现——不需要外部强制，权力已在内心运转（福柯）」

      - id: pan_power_automation
        name: 权力自动化
        age_range: [22, 45]
        weight: 0.5
        description: 「系统、算法、程序代替人执行监视——权力独立于人格化行使者」
        outcomes:
          power_automation: [+0.3, +0.4]
          stress_level: [+0.1, +0.2]
        sociological_reading: 「全景敞视使权力自动化——中心塔楼不再需要看守，囚犯自己看守自己（福柯）」

      - id: pan_anonymous_moment_loss
        name: 匿名时刻的丧失
        age_range: [20, 40]
        weight: 0.5
        description: 「在匿名论坛、陌生城市中发现自己不知道如何行为——自我规训已取代自发判断」
        outcomes:
          spontaneity: [-0.3, -0.4]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「匿名时刻的丧失是全景敞视成功的标志——即使在无监视的环境中权力依然运转（福柯）」

      - id: pan_medical_authority
        name: 医疗权威的裁决
        age_range: [18, 50]
        weight: 0.5
        description: 「医生的诊断即判决，处方即惩罚或赦免——医疗权威代替了对话和理解」
        outcomes:
          medical_authority: [+0.3, +0.4]
          stress_level: [+0.2, +0.4]
        sociological_reading: 「精神病院是全景敞视的典范——医疗权威成为新型的权力中心（福柯）」

      - id: pan_silence_regime
        name: 缄默制度
        age_range: [18, 45]
        weight: 0.4
        description: 「被剥夺对话权——无论说什么都被当作症状，话语在沉默中枯竭」
        outcomes:
          silence_regime: [+0.3, +0.4]
          stress_level: [+0.3, +0.5]
        sociological_reading: 「缄默是规训权力的极端形式——剥夺对话使谵妄在沉默中发酵（福柯）」

      - id: pan_mirror_recognition
        name: 镜像认识
        age_range: [18, 40]
        weight: 0.45
        description: 「在他人身上看到自己的异常——不是认同而是恐惧，镜子里反射的是疯癫本身」
        outcomes:
          mirror_recognition: [+0.3, +0.4]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「镜像认识是全景敞视的批判功能——在他人身上看到自己是规训的内化形式（福柯）」

      - id: pan_perpetual_judgment
        name: 永恒审判
        age_range: [18, 50]
        weight: 0.5
        description: 「每一个行为都被记录、评估、惩罚——审判不是为了正义而是为了生产持续的顺从」
        outcomes:
          perpetual_judgment: [+0.3, +0.4]
          stress_level: [+0.3, +0.4]
        sociological_reading: 「永恒审判是全景敞视的司法化——使权力效应在无判决的情况下持续（福柯）」

      - id: pan_insurance_algorithm
        name: 保险算法裁决
        age_range: [28, 50]
        weight: 0.45
        description: 「健康险、车险、寿险的保费由算法决定——基于不知道的数据做出无法理解的裁决」
        outcomes:
          data_footprint: [+0.2, +0.3]
          stress_level: [+0.2, +0.3]
        sociological_reading: 「保险算法是全景敞视对身体的延伸——生命本身变成可被计算的风险（福柯）」

      - id: pan_confession_extracted
        name: 被强制忏悔
        age_range: [15, 35]
        weight: 0.45
        description: 「被要求检讨、反省、写检查——忏悔成为规训技术，使主体主动生产自身」
        outcomes:
          internalized_surveillance: [+0.3, +0.4]
          stress_level: [+0.2, +0.4]
        sociological_reading: 「忏悔是规训权力的核心技术——通过使主体主动生产自身来行使控制（福柯）」

      - id: pan_data_exclusion
        name: 数据排斥——低分公民
        age_range: [20, 45]
        weight: 0.4
        description: 「评分跌入谷底后被主流数字服务排斥——成为现金社会的残余居民」
        outcomes:
          stress_level: [+0.4, +0.6]
          social_status: [-0.3, -0.4]
        sociological_reading: 「数据排斥是全景敞视的终极惩罚——被排除者成为社会看不见的幽灵（福柯）」

      - id: pan_body_self_surveillance
        name: 身体自我监视
        age_range: [25, 50]
        weight: 0.5
        description: 「健身打卡、饮食控制、睡眠监测——自我监视延伸到身体内部」
        outcomes:
          internalized_surveillance: [+0.3, +0.4]
          stress_level: [+0.1, +0.2]
        sociological_reading: 「身体是全景敞视最后的边疆——即使肉体也被纳入可被监视的范畴（福柯）」

      - id: pan_transparency_illusion
        name: 透明化的幻象
        age_range: [35, 60]
        weight: 0.45
        description: 「假想观众撤去后反而不知道如何行动——一生都在被看中确认自我」
        outcomes:
          spontaneity: [-0.2, -0.3]
          stress_level: [+0.1, -0.1]
        sociological_reading: 「透明化是全景敞视的最终胜利——主体在透明的幻象中丧失所有自发性（福柯）」

'''

# 追加到文件
content = content.rstrip()
new_content = content + disciplinary_power_events + panopticism_events + '\n'

with open('data/events.yaml', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Events appended successfully!')

# 验证
import yaml
with open('data/events.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

for cat in ['disciplinary_power', 'panopticism']:
    n = len(data['life_events'].get(cat, {}).get('events', []))
    print(f'{cat}: {n} events')

# 验证ASCII
bad = []
for cat, cat_data in data['life_events'].items():
    for e in cat_data.get('events', []):
        eid = e.get('id', '')
        if any(ord(c) > 127 for c in eid):
            bad.append(f'{cat}: {eid}')
if bad:
    print('NON-ASCII IDs:', bad)
else:
    print('All IDs ASCII-safe!')