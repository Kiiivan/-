"""
社会学人生模拟器 - 主应用
基于经典社会学理论的互动人生模拟游戏

玩家先选择宏观社会结构（出自社会学家的经典理论），
然后设定人物（性别、出生地等），系统根据这些设定随机生成
人物在这社会中一生的事迹。
"""
import os
import streamlit as st
import random
from modules.structure_engine import StructureEngine
from modules.character_gen import CharacterGenerator
from modules.life_generator import LifeGenerator
from modules.timeline import TimelineRenderer
from modules.social_rules import SocialRulesEngine

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="社会学人生模拟器",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 自定义样式
# ============================================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .structure-card {
        background: #f0f7f4;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        border-left: 4px solid #67c23a;
    }
    .event-card {
        background: #fafafa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #409eff;
    }
    .reading-card {
        background: #fef9ef;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.3rem 0;
        border-left: 4px solid #e6a23c;
        font-size: 0.9rem;
    }
    .stat-box {
        background: #f5f7fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    div.stButton > button:first-child {
        background-color: #409eff;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.4rem 1.5rem;
        font-weight: 500;
    }
    div.stButton > button:hover {
        background-color: #66b1ff;
        color: white;
    }
    .st-emotion-cache-v2zcq9 {
        background-color: #f5f7fa;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 初始化 session state
# ============================================================
def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "setup"
    if "character" not in st.session_state:
        st.session_state.character = None
    if "timeline" not in st.session_state:
        st.session_state.timeline = None
    if "metadata" not in st.session_state:
        st.session_state.metadata = None
    if "selected_structures" not in st.session_state:
        st.session_state.selected_structures = []
    if "life_result" not in st.session_state:
        st.session_state.life_result = None


def get_data_dir():
    """获取数据目录路径"""
    return os.path.join(os.path.dirname(__file__), "data")


# ============================================================
# 侧边栏：配置
# ============================================================
with st.sidebar:
    st.markdown("## 🎭 社会学人生模拟器")
    st.markdown("---")

    st.markdown("### 📚 社会学理论速览")
    st.markdown("""
    **涂尔干**：社会团结（机械/有机）、失范
    **韦伯**：社会行动四类型、理性化、祛魅
    **布迪厄**：文化资本、惯习、场域
    **福柯**：规训权力、全景敞视、生命政治
    **戈夫曼**：拟剧论、前台后台、印象管理
    **费孝通**：差序格局、礼治秩序、乡土性
    **贝克**：风险社会、反思性现代化
    **齐美尔**：形式社会学、陌生人、大都市
    **米尔斯**：社会学想象力
    """)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.8rem; color:#999;'>"
        "北京大学社会学系<br>"
        "「社会学的人工智能」课后实践"
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# 页面1：设置
# ============================================================
def render_setup_page():
    """渲染设置页面"""
    st.markdown('<p class="main-title">🎭 社会学人生模拟器</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">选择宏观社会结构，设定虚拟人物，体验社会理论如何影响个体命运</p>',
        unsafe_allow_html=True
    )

    # 初始化引擎
    data_dir = get_data_dir()
    structure_engine = StructureEngine(data_dir)
    character_gen = CharacterGenerator(data_dir)

    # ============================================================
    # 第一步：选择社会结构
    # ============================================================
    st.markdown("## 第一步：选择宏观社会结构")

    # 显示社会结构关系网络图（预生成PNG）
    import os
    data_dir = get_data_dir()
    network_img_path = os.path.join(data_dir, "structure_network.png")

    # 弹窗放大查看功能
    @st.dialog("📊 社会结构关系网络图", width="large")
    def show_network_fullscreen():
        if os.path.exists(network_img_path):
            st.image(network_img_path, use_container_width=True)
            st.markdown("""
            **图例说明：**
            - 🔴 红色系：涂尔干（机械团结、有机团结）
            - 🔵 蓝色系：韦伯（理性化、祛魅）
            - 🟣 紫色系：布迪厄（高压场域、高/低文化资本）
            - 🟠 橙色系：福柯（规训社会、全景敞视）
            - 🟢 绿色系：费孝通（乡土社会）
            - 🟡 黄色系：贝克（风险社会）
            - 🔷 青色系：齐美尔（大都市、陌生人）
            - 绿色实线 = 相生关系（互相促进）
            - 红色虚线 = 相克关系（互相矛盾）
            """)
        else:
            st.info("网络图文件不存在")

    with st.expander("📊 社会结构关系网络图（点击展开）"):
        if os.path.exists(network_img_path):
            # 缩略图（宽度收窄）
            st.image(network_img_path, use_container_width=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🔍 放大查看大图", use_container_width=True):
                    show_network_fullscreen()
            with col2:
                # 提供交互版下载链接
                html_path = os.path.join(data_dir, "structure_network.html")
                if os.path.exists(html_path):
                    with open(html_path, "rb") as f:
                        st.download_button(
                            "📥 下载交互版HTML",
                            f.read(),
                            file_name="structure_network.html",
                            mime="text/html",
                        )
            st.markdown("""
            **图例说明：**
            - 🔴 涂尔干 | 🔵 韦伯 | 🟣 布迪厄 | 🟠 福柯 | 🟢 费孝通 | 🟡 贝克 | 🔷 齐美尔
            - 绿色实线 = 相生  |  红色虚线 = 相克
            """)
        else:
            st.info("网络图尚未生成，将在首次加载时创建")

    st.info("💡 选择2-4个社会结构，它们会相互作用，影响人物的人生轨迹")

    # 按理论家分组展示
    structures_by_theorist = structure_engine.get_structures_by_category()

    selected_structures = []

    cols = st.columns(2)
    for i, (theorist, structures) in enumerate(structures_by_theorist.items()):
        with cols[i % 2]:
            st.markdown(f"### {theorist}")
            for s in structures:
                checked = st.checkbox(
                    f"{s['emoji']} {s['name']}",
                    value=False,
                    key=f"struct_{s['id']}",
                    help=f"{s['description'][:50]}..."
                )
                if checked:
                    selected_structures.append(s["id"])

    st.markdown("---")

    # ============================================================
    # 第二步：设定人物
    # ============================================================
    st.markdown("## 第二步：设定虚拟人物")

    tab_preset, tab_custom = st.tabs(["🎭 预设人物", "✏️ 自定义"])

    with tab_preset:
        presets = character_gen.get_preset_characters()
        preset_options = [""] + [f"{p['emoji']} {p['name']}" for p in presets]
        selected_preset = st.selectbox(
            "选择预设人物（快速开始）",
            preset_options,
            format_func=lambda x: x if x else "请选择..."
        )

        if selected_preset:
            preset_id = selected_preset.split(" ", 1)[1] if " " in selected_preset else ""
            # 查找匹配的预设
            for p in presets:
                if p["name"] == preset_id or f"{p['emoji']} {p['name']}" == selected_preset:
                    st.markdown(f"**{p['description']}**")
                    break

    with tab_custom:
        col1, col2 = st.columns(2)

        with col1:
            gender_options = character_gen.get_gender_options()
            gender_choice = st.selectbox(
                "性别",
                range(len(gender_options)),
                format_func=lambda i: f"{gender_options[i]['emoji']} {gender_options[i]['name']}"
            )

            birth_place_options = character_gen.get_birth_place_options()
            birth_place_choice = st.selectbox(
                "出生地类型",
                range(len(birth_place_options)),
                format_func=lambda i: f"{birth_place_options[i]['emoji']} {birth_place_options[i]['name']}"
            )

        with col2:
            era_options = character_gen.get_era_options()
            era_choice = st.selectbox(
                "时代背景",
                range(len(era_options)),
                format_func=lambda i: f"{era_options[i]['emoji']} {era_options[i]['name']}"
            )

            parent_class_options = character_gen.get_parent_class_options()
            parent_class_choice = st.selectbox(
                "父母阶层",
                range(len(parent_class_options)),
                format_func=lambda i: f"{parent_class_options[i]['emoji']} {parent_class_options[i]['name']}"
            )

    st.markdown("---")

    # ============================================================
    # 第三步：生成模拟
    # ============================================================
    st.markdown("## 第三步：生成人生模拟")

    random_seed = st.number_input(
        "随机种子（相同种子产生相同结果）",
        min_value=0,
        max_value=999999,
        value=random.randint(1, 999999),
        step=1
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button(
            "🚀 开始模拟人生",
            use_container_width=True
        )

    if generate_button:
        if len(selected_structures) < 2:
            st.error("请至少选择2个社会结构")
            return

        # 强制清除所有session state
        for key in list(st.session_state.keys()):
            if key not in ['page']:
                del st.session_state[key]

        # 显示社会规则预览
        social_rules_engine = SocialRulesEngine(data_dir)
        social_rules = social_rules_engine.generate_social_rules(selected_structures)

        st.markdown("---")
        st.markdown("## 🌍 社会规则预览")
        st.markdown(f"### {social_rules['name']}")

        # 显示规则说明
        edu = social_rules.get("education", {})
        work = social_rules.get("work", {})
        marriage = social_rules.get("marriage", {})

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**📚 教育制度**")
            st.markdown(f"- 入学年龄：{edu.get('school_start_age', 6)}岁")
            st.markdown(f"- 小学：{edu.get('primary_years', 6)}年")
            st.markdown(f"- 初中：{edu.get('middle_years', 3)}年")
            st.markdown(f"- 高中：{edu.get('high_years', 3)}年")
            st.markdown(f"- 大学：{edu.get('university_years', 4)}年")

        with col2:
            st.markdown("**💼 工作制度**")
            st.markdown(f"- 最低工作年龄：{work.get('min_age', 16)}岁")
            st.markdown(f"- 典型首份工作：{work.get('typical_first_job', 18)}岁")
            st.markdown(f"- 法定退休年龄：{work.get('retirement_age', 60)}岁")

        with col3:
            st.markdown("**💒 婚姻制度**")
            st.markdown(f"- 法定婚龄：{marriage.get('legal_age', 22)}岁")
            st.markdown(f"- 包办婚姻比例：{int(marriage.get('arranged_ratio', 0.2)*100)}%")

        # 显示社会特征
        st.markdown("**🏷️ 这个社会的特殊规则：**")
        for struct_id in selected_structures:
            struct = structure_engine.get_structure(struct_id)
            if struct:
                st.markdown(f"- {struct['emoji']} {struct['name']}：{struct['description'][:30]}...")

        st.markdown("---")

        # 生成人物
        if selected_preset:
            # 使用预设人物
            for p in character_gen.get_preset_characters():
                if f"{p['emoji']} {p['name']}" == selected_preset:
                    character = character_gen.apply_preset(p["id"])
                    break
        else:
            # 使用自定义设定
            gender_id = gender_options[gender_choice]["id"]
            birth_place_id = birth_place_options[birth_place_choice]["id"]
            era_id = era_options[era_choice]["id"]
            parent_class_id = parent_class_options[parent_class_choice]["id"]

            character = character_gen.generate_character(
                gender_id=gender_id,
                birth_place_id=birth_place_id,
                era_id=era_id,
                parent_class_id=parent_class_id
            )

        # 生成时间线
        life_gen = LifeGenerator(data_dir)
        result = life_gen.generate_timeline_with_visualization(
            character=character,
            selected_structure_ids=selected_structures,
            seed=random_seed
        )

        # 保存到session state
        st.session_state.character = character
        st.session_state.timeline = result["timeline"]
        st.session_state.metadata = result["metadata"]
        st.session_state.selected_structures = selected_structures
        st.session_state.life_result = result

        st.session_state.page = "result"
        st.rerun()


# ============================================================
# 页面2：结果展示
# ============================================================
def render_result_page():
    """渲染结果页面"""
    character = st.session_state.character
    timeline = st.session_state.timeline
    metadata = st.session_state.metadata
    selected_structures = st.session_state.selected_structures

    if not character or not timeline:
        st.error("没有可显示的结果，请先运行模拟")
        if st.button("返回重新设置"):
            st.session_state.page = "setup"
            st.rerun()
        return

    # 头部信息
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"## 📜 {character['name']}的人生年表")
        st.markdown(f"""
        **出生年份**：约{character['birth_year']}年 |
        **性别**：{character.get('gender_display', character['gender'])} |
        **出生地**：{character.get('birth_place_display', character['birth_place'])}
        """)
    with col2:
        if st.button("🔄 重新模拟"):
            st.session_state.page = "setup"
            st.rerun()

    st.markdown("---")

    # 统计概览
    st.markdown("### 📊 人生统计")
    stats_cols = st.columns(4)
    with stats_cols[0]:
        st.metric("总事件数", len(timeline))
    with stats_cols[1]:
        ages = [e.get("age", 0) for e in timeline]
        life_span = max(ages) - min(ages) if ages else 0
        st.metric("人生跨度", f"{life_span}年")
    with stats_cols[2]:
        attrs = character.get("attributes", {})
        edu_level = int(attrs.get("education_level", 0))
        edu_labels = ["文盲", "小学", "初中", "高中", "大专/本科", "研究生"]
        st.metric("初始学历", edu_labels[min(edu_level, 5)])
    with stats_cols[3]:
        final_age = max([e.get("age", 0) for e in timeline]) if timeline else 0
        st.metric("终老年龄", f"{final_age}岁")

    st.markdown("---")

    # 社会规则预览
    data_dir = get_data_dir()
    social_rules_engine = SocialRulesEngine(data_dir)
    social_rules = social_rules_engine.generate_social_rules(selected_structures)

    st.markdown("### 🌍 社会规则预览")
    st.markdown(f"**社会名称**：{social_rules['name']}")

    edu = social_rules.get("education", {})
    work = social_rules.get("work", {})
    marriage = social_rules.get("marriage", {})

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📚 教育制度**")
        st.markdown(f"- 入学年龄：{edu.get('school_start_age', 6)}岁")
        st.markdown(f"- 小学：{edu.get('primary_years', 6)}年")
        st.markdown(f"- 初中：{edu.get('middle_years', 3)}年")
        st.markdown(f"- 高中：{edu.get('high_years', 3)}年")
        st.markdown(f"- 大学：{edu.get('university_years', 4)}年")
    with col2:
        st.markdown("**💼 工作制度**")
        st.markdown(f"- 最低工作年龄：{work.get('min_age', 16)}岁")
        st.markdown(f"- 典型首份工作：{work.get('typical_first_job', 18)}岁")
        st.markdown(f"- 法定退休年龄：{work.get('retirement_age', 60)}岁")
    with col3:
        st.markdown("**💒 婚姻制度**")
        st.markdown(f"- 法定婚龄：{marriage.get('legal_age', 22)}岁")
        st.markdown(f"- 包办婚姻比例：{int(marriage.get('arranged_ratio', 0.2)*100)}%")

    st.markdown("---")

    # 社会结构说明
    with st.expander("📚 本次模拟的社会结构详情"):
        data_dir = get_data_dir()
        structure_engine = StructureEngine(data_dir)
        st.markdown(structure_engine.get_structural_summary(selected_structures))

    st.markdown("---")

    # 时间线展示
    st.markdown("### ⏳ 人生时间线（按年龄排序）")

    # 按年龄分组显示
    age_groups = {}
    for event in timeline:
        age = event.get("age", 0)
        if age not in age_groups:
            age_groups[age] = []
        age_groups[age].append(event)

    # 显示每个年龄的事件
    for age in sorted(age_groups.keys()):
        events_at_age = age_groups[age]
        for event in events_at_age:
            with st.container():
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(f"### {event.get('action_emoji', '📋')}")
                    st.markdown(f"**{age}岁**")
                with col2:
                    st.markdown(f"#### {event['name']}")
                    st.markdown(event.get('description', ''))
                    # 社会学解读
                    reading = event.get("sociological_reading", "")
                    if reading:
                        st.markdown(f"📚 *{reading}*")
            st.markdown("---")

    st.markdown("---")

    # 人生故事
    st.markdown("### 📖 人生故事")

    renderer = TimelineRenderer()
    life_story = renderer.generate_life_story_text(timeline, character)
    st.markdown(life_story)

    # 行动类型分析
    st.markdown("### 🎭 主导行动类型分析")

    actions = metadata.get("dominant_actions", {})
    if actions:
        action_labels = {
            "affective_action": "情感行动",
            "value_rational_action": "价值理性行动",
            "instrumental_rational_action": "工具理性行动",
            "traditional_action": "传统行动",
            "habitus_guided_action": "惯习引导行动",
            "capital_competition": "资本竞争行动",
            "impression_management_action": "印象管理行动",
            "anomie_action": "失范行动",
        }

        action_cols = st.columns(min(len(actions), 4))
        for i, (action_id, count) in enumerate(actions.items()):
            with action_cols[i % 4]:
                label = action_labels.get(action_id, action_id)
                st.markdown(f"**{label}**：{count}次")


# ============================================================
# 主程序入口
# ============================================================
def main():
    init_session_state()

    if st.session_state.page == "setup":
        render_setup_page()
    elif st.session_state.page == "result":
        render_result_page()


if __name__ == "__main__":
    main()
