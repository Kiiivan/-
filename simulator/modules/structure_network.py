"""
Structure Relationship Network Generator - Matplotlib Version with Chinese
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Dict, List, Tuple
import os

# Use non-GUI backend
plt.switch_backend('Agg')

# Chinese name mapping
STRUCTURE_NAMES_CN = {
    "mechanical_solidarity": "机械团结",
    "organic_solidarity": "有机团结",
    "rationalization": "理性化",
    "disenchantment": "祛魅",
    "field_pressure_high": "高压场域",
    "cultural_capital_high": "高文化资本",
    "cultural_capital_low": "低文化资本",
    "disciplinary_power": "规训社会",
    "panopticism": "全景敞视",
    "rural_china": "乡土社会",
    "risk_society": "风险社会",
    "metropolis": "大都市",
    "stranger_status": "陌生人",
}

# Theorist mapping
STRUCTURE_THEORISTS = {
    "mechanical_solidarity": "涂尔干",
    "organic_solidarity": "涂尔干",
    "rationalization": "韦伯",
    "disenchantment": "韦伯",
    "field_pressure_high": "布迪厄",
    "cultural_capital_high": "布迪厄",
    "cultural_capital_low": "布迪厄",
    "disciplinary_power": "福柯",
    "panopticism": "福柯",
    "rural_china": "费孝通",
    "risk_society": "贝克",
    "metropolis": "齐美尔",
    "stranger_status": "齐美尔",
}

# 13 sociological structure nodes
# Using \UXXXXXXXX for non-BMP emoji (above U+FFFF) to avoid surrogate issues
STRUCTURE_NODES = {
    "mechanical_solidarity": {"emoji": "\U0001F517", "color": "#e74c3c", "shortLabel": "机械"},
    "organic_solidarity": {"emoji": "\U0001F504", "color": "#e74c3c", "shortLabel": "有机"},
    "rationalization": {"emoji": "⚙", "color": "#3498db", "shortLabel": "理性化"},
    "disenchantment": {"emoji": "\U0001F32B", "color": "#3498db", "shortLabel": "祛魅"},
    "field_pressure_high": {"emoji": "\U0001F3DB", "color": "#9b59b6", "shortLabel": "高压场域"},
    "cultural_capital_high": {"emoji": "\U0001F4DA", "color": "#9b59b6", "shortLabel": "高文化"},
    "cultural_capital_low": {"emoji": "\U0001F4D6", "color": "#9b59b6", "shortLabel": "低文化"},
    "disciplinary_power": {"emoji": "\U0001F441", "color": "#e67e22", "shortLabel": "规训"},
    "panopticism": {"emoji": "\U0001F3E5", "color": "#e67e22", "shortLabel": "全景"},
    "rural_china": {"emoji": "\U0001F33E", "color": "#27ae60", "shortLabel": "乡土"},
    "risk_society": {"emoji": "⚠", "color": "#f39c12", "shortLabel": "风险"},
    "metropolis": {"emoji": "\U0001F306", "color": "#1abc9c", "shortLabel": "大都市"},
    "stranger_status": {"emoji": "\U0001F310", "color": "#1abc9c", "shortLabel": "陌生人"},
}

# Structure relations
STRUCTURE_RELATIONS = [
    ("mechanical_solidarity", "organic_solidarity", -0.8, "conflict"),
    ("rationalization", "disenchantment", 0.6, "synergy"),
    ("field_pressure_high", "cultural_capital_high", 0.4, "synergy"),
    ("cultural_capital_high", "cultural_capital_low", -0.8, "conflict"),
    ("disciplinary_power", "panopticism", 0.7, "synergy"),
    ("metropolis", "stranger_status", 0.6, "synergy"),
    ("metropolis", "rationalization", 0.4, "synergy"),
    ("mechanical_solidarity", "disenchantment", -0.5, "conflict"),
    ("mechanical_solidarity", "rationalization", -0.4, "conflict"),
    ("organic_solidarity", "rationalization", 0.3, "synergy"),
    ("mechanical_solidarity", "cultural_capital_low", 0.3, "synergy"),
    ("organic_solidarity", "field_pressure_high", 0.3, "synergy"),
    ("mechanical_solidarity", "rural_china", 0.6, "synergy"),
    ("rural_china", "organic_solidarity", -0.4, "conflict"),
    ("mechanical_solidarity", "metropolis", -0.5, "conflict"),
    ("rationalization", "disciplinary_power", 0.4, "synergy"),
    ("rationalization", "risk_society", 0.3, "synergy"),
    ("field_pressure_high", "disciplinary_power", 0.4, "synergy"),
    ("cultural_capital_high", "disciplinary_power", 0.3, "synergy"),
    ("cultural_capital_high", "metropolis", 0.4, "synergy"),
    ("field_pressure_high", "metropolis", 0.3, "synergy"),
    ("rural_china", "risk_society", -0.3, "conflict"),
    ("rural_china", "metropolis", -0.6, "conflict"),
    ("rural_china", "stranger_status", -0.5, "conflict"),
    ("risk_society", "metropolis", 0.4, "synergy"),
    ("risk_society", "stranger_status", 0.3, "synergy"),
    ("risk_society", "panopticism", 0.4, "synergy"),
    ("risk_society", "disciplinary_power", 0.3, "synergy"),
    ("organic_solidarity", "risk_society", 0.3, "synergy"),
    ("cultural_capital_high", "risk_society", 0.2, "synergy"),
]


def get_theorist_color(theorist: str) -> str:
    colors = {
        "涂尔干": "#e74c3c",
        "韦伯": "#3498db",
        "布迪厄": "#9b59b6",
        "福柯": "#e67e22",
        "费孝通": "#27ae60",
        "贝克": "#f39c12",
        "齐美尔": "#1abc9c",
    }
    return colors.get(theorist, "#95a5a6")


def get_conflicts_for(structure_id: str) -> List[str]:
    """Get structures that conflict with the given structure"""
    conflicts = []
    for source, target, weight, rel_type in STRUCTURE_RELATIONS:
        if rel_type == "conflict":
            if source == structure_id:
                conflicts.append(target)
            elif target == structure_id:
                conflicts.append(source)
    return conflicts


def get_synergies_for(structure_id: str) -> List[str]:
    """Get structures that synergize with the given structure"""
    synergies = []
    for source, target, weight, rel_type in STRUCTURE_RELATIONS:
        if rel_type == "synergy":
            if source == structure_id:
                synergies.append(target)
            elif target == structure_id:
                synergies.append(source)
    return synergies


def generate_network_image(output_path: str = None) -> str:
    """Generate structure network diagram with Chinese labels"""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..", "data", "structure_network.png")

    # Set font for Chinese (priority) and emoji (fallback for emoji glyphs)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots(1, 1, figsize=(16, 12))

    # Node positions
    node_positions = {
        "mechanical_solidarity": (0.5, 0.8),
        "organic_solidarity": (0.5, 0.2),
        "rationalization": (2.0, 0.9),
        "disenchantment": (3.2, 0.9),
        "field_pressure_high": (4.5, 0.85),
        "cultural_capital_high": (5.5, 0.95),
        "cultural_capital_low": (5.5, 0.65),
        "disciplinary_power": (4.0, 0.35),
        "panopticism": (5.2, 0.35),
        "rural_china": (1.0, 0.15),
        "risk_society": (2.5, 0.25),
        "metropolis": (3.5, 0.1),
        "stranger_status": (4.5, 0.1),
    }

    # Draw edges
    for source, target, weight, rel_type in STRUCTURE_RELATIONS:
        if source not in node_positions or target not in node_positions:
            continue

        x1, y1 = node_positions[source]
        x2, y2 = node_positions[target]

        if rel_type == "synergy":
            color = "#27ae60"
            alpha = min(0.8, 0.3 + abs(weight) * 0.5)
            linewidth = 1 + abs(weight) * 2
            linestyle = '-'
        else:
            color = "#e74c3c"
            alpha = min(0.8, 0.3 + abs(weight) * 0.5)
            linewidth = 1 + abs(weight) * 2
            linestyle = '--'

        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->",
                color=color,
                alpha=alpha,
                lw=linewidth,
                linestyle=linestyle,
                shrinkA=25,
                shrinkB=25,
            ),
        )

    # Draw nodes
    for node_id, pos in node_positions.items():
        info = STRUCTURE_NODES[node_id]
        color = info["color"]
        name = STRUCTURE_NAMES_CN[node_id]
        theorist = STRUCTURE_THEORISTS[node_id]

        circle = plt.Circle(pos, 0.12, color=color, alpha=0.85, zorder=3)
        ax.add_patch(circle)

        circle_outline = plt.Circle(pos, 0.12, fill=False, edgecolor='white', linewidth=2, zorder=3)
        ax.add_patch(circle_outline)

        # Emoji above circle (emoji font)
        ax.text(pos[0], pos[1] + 0.04, info['emoji'], ha='center', va='center',
                fontsize=11, fontweight='bold', zorder=5,
                fontfamily='Segoe UI Emoji')

        # Chinese name inside circle (Chinese font) - use shortLabel for compact display
        ax.text(pos[0], pos[1] - 0.01, info['shortLabel'], ha='center', va='center',
                fontsize=8, fontweight='bold', color='white', zorder=5)

        ax.text(pos[0], pos[1] - 0.2, f"[{node_id}]", ha='center', va='top',
                fontsize=6, color='#555', zorder=4)

    # Legend - 移到右下角，不遮挡网络
    legend_elements = [
        mpatches.Patch(color="#27ae60", label="绿色实线 = 相生关系（互相促进）"),
        mpatches.Patch(color="#e74c3c", label="红色虚线 = 相克关系（互相矛盾）"),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.9,
              borderaxespad=0.5)

    # 理论家颜色图例 - 横向排列在底部
    theorist_legend_items = [
        mpatches.Patch(color="#e74c3c", label="涂尔干"),
        mpatches.Patch(color="#3498db", label="韦伯"),
        mpatches.Patch(color="#9b59b6", label="布迪厄"),
        mpatches.Patch(color="#e67e22", label="福柯"),
        mpatches.Patch(color="#27ae60", label="费孝通"),
        mpatches.Patch(color="#f39c12", label="贝克"),
        mpatches.Patch(color="#1abc9c", label="齐美尔"),
    ]
    legend2 = ax.legend(handles=theorist_legend_items, loc='lower left',
                       fontsize=9, framealpha=0.9, title='理论家', title_fontsize=9,
                       borderaxespad=0.5)
    ax.add_artist(legend2)

    # Title
    ax.set_title(
        "社会学宏观结构关系网络图\n13个结构间的相生相克",
        fontsize=18,
        fontweight='bold',
        pad=20
    )

    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.2, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')

    # Theorist labels
    theorist_labels = [
        (0.5, 1.05, "涂尔干", "#e74c3c"),
        (2.6, 1.05, "韦伯", "#3498db"),
        (5.0, 1.05, "布迪厄", "#9b59b6"),
        (4.6, 0.55, "福柯", "#e67e22"),
        (1.0, 0.05, "费孝通", "#27ae60"),
        (2.5, 0.05, "贝克", "#f39c12"),
        (4.0, -0.05, "齐美尔", "#1abc9c"),
    ]
    for x, y, text, color in theorist_labels:
        ax.text(x, y, text, ha='center', va='bottom', fontsize=10,
                color=color, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()

    return output_path


def generate_interactive_network_html(output_path: str = None) -> str:
    """Generate interactive HTML network with click-to-explore interaction.
    Uses all-plain-ASCII output to avoid any encoding issues."""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..", "data", "structure_network.html")

    import json

    # WHY explanations: why these two structures have the given relationship
    WHY = {
        ("mechanical_solidarity", "organic_solidarity"): "涂尔干认为机械团结基于成员相似性（共同意识），有机团结基于劳动分工与社会差异。两者是社会团结的两种截然不同的机制，难以同时主导同一社会。",
        ("rationalization", "disenchantment"): "韦伯的理性化（工具理性）必然带来祛魅——世界的理性化解除了宗教和传统的魔法，理性化本身就是祛魅的原因。",
        ("field_pressure_high", "cultural_capital_high"): "布迪厄：场域压力越大，个体越需要积累文化资本来获得合法性与竞争力，高压场域是文化资本积累的直接动力。",
        ("cultural_capital_high", "cultural_capital_low"): "文化资本是稀缺资源，其分布是零和的：高文化资本者必然占据优势位置，低资本者则处于被支配地位。",
        ("disciplinary_power", "panopticism"): "福柯：规训权力的核心机制是全景敞视——被监视者将监视内化为自我规训，两者是一体两面。",
        ("metropolis", "stranger_status"): "齐美尔：大都市是陌生人密集居住的空间，陌生人关系是大都市的基本社会形态，人口流动性使每个人都成为潜在的陌生人。",
        ("metropolis", "rationalization"): "齐美尔：大都市的货币经济推动了理性化计算，货币作为理性化的媒介在大都市中充分发展。",
        ("mechanical_solidarity", "disenchantment"): "机械团结依赖共同信仰与传统权威，祛魅瓦解了共同意识的基础，两者处于根本对立。",
        ("mechanical_solidarity", "rationalization"): "机械团结基于传统与习俗，理性化要求以工具理性取代传统权威，两者不相容。",
        ("organic_solidarity", "rationalization"): "有机团结依赖劳动分工，理性化（官僚制与专业化）深化了分工，两者互相加强。",
        ("mechanical_solidarity", "cultural_capital_low"): "机械团结社会中文化教育不重要，低文化资本者是主体；文化资本竞争在这些社会中尚未成为核心议题。",
        ("organic_solidarity", "field_pressure_high"): "有机团结社会的复杂分工产生更多场域，劳动分化带来阶层分化，从而增强场域压力。",
        ("mechanical_solidarity", "rural_china"): "费孝通：乡土社会以长老统治和礼治为特征，与机械团结（共同意识主导）高度吻合，差序格局体现机械团结。",
        ("rural_china", "organic_solidarity"): "费孝通的差序格局强调熟人关系，有机团结以契约为基础的分工与熟人信任机制冲突。",
        ("mechanical_solidarity", "metropolis"): "机械团结依赖集体意识与共同记忆，大都市的匿名性和多元性瓦解了集体意识的基础。",
        ("rationalization", "disciplinary_power"): "韦伯的理性化与福柯的规训权力紧密相连——理性化的官僚制本身就是规训机构，量化评估是规训的基础。",
        ("rationalization", "risk_society"): "韦伯的理性化是贝克风险社会的条件之一：理性化产生系统性风险，而反思性现代化则是对理性化风险的自觉。",
        ("field_pressure_high", "disciplinary_power"): "布迪厄的场域逻辑与福柯的规训权力共谋：场域中的权力通过规训技术维持支配关系。",
        ("cultural_capital_high", "disciplinary_power"): "高文化资本者更擅长自我规训（内化场域规则），规训权力因此对他们更为隐蔽而有效。",
        ("cultural_capital_high", "metropolis"): "大都市提供更多文化消费机会，高文化资本者利用其资本优势更好地利用城市资源。",
        ("field_pressure_high", "metropolis"): "大都市的阶层分化最为明显，场域压力（竞争、身份焦虑）在城市空间中更为集中和剧烈。",
        ("rural_china", "risk_society"): "费孝通的乡土社会依靠传统和礼治，贝克的风险社会是反思现代化的产物，乡土社会的稳定性与风险社会的不确定性相冲突。",
        ("rural_china", "metropolis"): "费孝通的差序格局建立在熟人信任基础上，大都市的陌生人社会与乡土熟人社会在社会结构上根本对立。",
        ("rural_china", "stranger_status"): "费孝通乡土社会的信任基于血缘和地缘，陌生人（无根基的流动者）打破了这种熟人信任模式。",
        ("risk_society", "metropolis"): "贝克：风险社会的风险具有全球性和匿名性，大都市是风险最集中、最可见的空间，同时大都市也是应对风险的资源池。",
        ("risk_society", "stranger_status"): "贝克：风险社会中每个人都生活在不确定性中，陌生人天然处于风险前沿，缺乏社会网络保护。",
        ("risk_society", "panopticism"): "贝克的风险社会与福柯的全景敞视都强调对人口的监控与管理，规训权力通过制造和管理风险维持控制。",
        ("risk_society", "disciplinary_power"): "风险社会的专家系统本身成为新的规训权力来源，专业知识通过制造风险感来控制大众行为。",
        ("organic_solidarity", "risk_society"): "有机团结的分工越复杂，社会相互依赖越强，系统性风险（如金融危机）的传播范围也越广。",
        ("cultural_capital_high", "risk_society"): "高文化资本者具备更多风险认知能力和社会资源，在风险社会中占据优势地位。",
    }

    # Build edgesMeta (for info panel) and edges (for vis.js)
    edges_meta = {}
    edges_data = []  # plain JS object strings
    for idx, (source, target, weight, rel_type) in enumerate(STRUCTURE_RELATIONS):
        eid = "e%d" % idx
        from_name = STRUCTURE_NAMES_CN[source]
        to_name = STRUCTURE_NAMES_CN[target]
        theorist_a = STRUCTURE_THEORISTS[source]
        theorist_b = STRUCTURE_THEORISTS[target]
        color_a = STRUCTURE_NODES[source]["color"]
        color_b = STRUCTURE_NODES[target]["color"]

        a_conflicts = get_conflicts_for(source)
        a_synergies = get_synergies_for(source)
        b_conflicts = get_conflicts_for(target)
        b_synergies = get_synergies_for(target)

        if rel_type == "synergy":
            line_color = "#27ae60"
            dashes = "false"
            width_val = 1.0 + abs(weight) * 3.0
            rel_label = "XiangSheng"   # 相生
            rel_label_cn = "相生关系"
            rel_desc = "These two structures promote each other and coexist."
            rel_desc_cn = "这两个社会结构互相促进，可以共存并相互强化。"
        else:
            line_color = "#c0392b"
            dashes = "true"
            width_val = 1.0 + abs(weight) * 3.0
            rel_label = "XiangKe"   # 相克
            rel_label_cn = "相克关系"
            rel_desc = "These two structures conflict and cannot coexist."
            rel_desc_cn = "这两个社会结构互相矛盾，难以并存，选择时需注意。"

        edges_meta[eid] = {
            "from": source, "to": target,
            "fn": from_name, "tn": to_name,
            "ta": theorist_a, "tb": theorist_b,
            "ca": color_a, "cb": color_b,
            "rt": rel_type,
            "rl": rel_label, "rlc": rel_label_cn,
            "rd": rel_desc, "rdc": rel_desc_cn,
            "ac": a_conflicts, "as": a_synergies,
            "bc": b_conflicts, "bs": b_synergies,
            "why": WHY.get((source, target), WHY.get((target, source), "社会学理论关联。")),
        }

        edges_data.append(
            "{id:'%s',from:'%s',to:'%s',color:{color:'%s',highlight:'%s',opacity:0.7},dashes:%s,width:%.1f,arrows:{to:{enabled:true,scaleFactor:0.3}},smooth:{type:'continuous'}}"
            % (eid, source, target, line_color, line_color, dashes, width_val)
        )

    # Build nodes - label is FULL name, positioned BELOW the dot (outside colored area)
    nodes_data = []
    for nid, info in STRUCTURE_NODES.items():
        full_name = STRUCTURE_NAMES_CN[nid]   # full name for label
        col = info["color"]
        nodes_data.append(
            '{id:"%s",label:"%s",color:"%s",font:{color:"#222",size:13,face:"Microsoft YaHei",bold:false},shape:"dot",borderWidth:2,borderWidthSelected:4,shadow:true}'
            % (nid, full_name, col)
        )

    # Serialize to JSON (only ASCII chars in values after ensure_ascii)
    edges_meta_json = json.dumps(edges_meta, ensure_ascii=True)

    # Build JS: edgesMeta + nodes + edges + interaction
    # Use ASCII keys in JS too to avoid any encoding issues
    js_lines = [
        "(function(){",
        "var EM=" + edges_meta_json + ";",
        "var NAMES=" + json.dumps(STRUCTURE_NAMES_CN, ensure_ascii=True) + ";",
        "var nodes=new vis.DataSet([%s]);" % ",".join(nodes_data),
        "var edges=new vis.DataSet([%s]);" % ",".join(edges_data),
        "var net=new vis.Network(document.getElementById('n'),{nodes:nodes,edges:edges},{",
        "  nodes:{shape:'dot',size:18,borderWidth:2,shadow:true,",
        "        color:{background:'#666',border:'#fff',highlight:{background:'#888',border:'#fff'}}},",
        "  physics:{enabled:true,solver:'forceAtlas2Based',",
        "           forceAtlas2Based:{gravitationalConstant:-50,centralGravity:0.01,",
        "                            springLength:130,springConstant:0.08,damping:0.4},",
        "           stabilization:{iterations:150}},",
        "  interaction:{hover:false,zoomView:true,dragView:true}",
        "});",
        "var sel=null;",
        "function tag(arr,t){",
        "  if(!arr||!arr.length)return'<span style=\"color:#bbb;font-size:11px;\">none</span>';",
        "  return arr.map(function(c){",
        "    var n=NAMES[c]||c;",
        "    var bg=t==='conflict'?'#fde8e8':'#e8f8f0';",
        "    var cl=t==='conflict'?'#c0392b':'#27ae60';",
        "    return'<span style=\"background:'+bg+';color:'+cl+';padding:1px 6px;border-radius:8px;font-size:11px;\">'+n+'</span>';",
        "  }).join('');",
        "}",
        "function dimAll(){edges.forEach(function(e){",
        "  var m=EM[e.id];if(!m)return;",
        "  var c=m.rt==='synergy'?'#27ae60':'#c0392b';",
        "  edges.update({id:e.id,color:{color:c,highlight:c,opacity:0.1},width:1});",
        "});}",
        "function hl(eid){var m=EM[eid];if(!m)return;",
        "  var c=m.rt==='synergy'?'#27ae60':'#c0392b';",
        "  edges.update({id:eid,color:{color:c,highlight:c,opacity:1},width:3});",
        "}",
        "function show(eid){var m=EM[eid];if(!m)return;",
        "  var rb=m.rt==='synergy'?'#e8f8f0':'#fde8e8';",
        "  var rc=m.rt==='synergy'?'#27ae60':'#c0392b';",
        "  var st=Math.abs(m.weight||0.5)>0.5?'Strong':'Weak';",
        "  var why=m.why||'';",
        "  var html='<div style=\"font-size:14px;font-weight:bold;color:#333;border-bottom:2px solid #eee;padding-bottom:8px;margin-bottom:10px;\">Theory Relation</div>';",
        "  html+='<div style=\"border-radius:8px;padding:10px 12px;margin-bottom:10px;border-left:3px solid '+m.ca+';\">';",
        "  html+='<div style=\"font-size:14px;font-weight:bold;\">'+m.fn+'</div>';",
        "  html+='<div style=\"font-size:12px;opacity:0.75;\">Theorist: '+m.ta+'</div>';",
        "  html+='<div style=\"font-size:12px;color:#666;margin-bottom:3px;\">Conflicts: '+tag(m.ac,'conflict')+'</div>';",
        "  html+='<div style=\"font-size:12px;color:#666;\">Synergies: '+tag(m.as,'synergy')+'</div></div>';",
        "  html+='<div style=\"display:inline-block;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:bold;background:'+rb+';color:'+rc+';\">'+m.rl+' ('+st+')</div>';",
        "  html+='<div style=\"font-size:12px;line-height:1.6;color:#555;margin-bottom:10px;\">'+m.rdc+'</div>';",
        "  if(why){html+='<div style=\"background:#fffbe6;border:1px solid #f0c060;border-radius:8px;padding:10px 12px;margin-bottom:10px;\">';",
        "  html+='<div style=\"font-size:12px;font-weight:bold;color:#856404;margin-bottom:5px;\">Why?</div>';",
        "  html+='<div style=\"font-size:12px;line-height:1.6;color:#856404;\">'+why+'</div></div>';",
        "  }",
        "  html+='<div style=\"border-radius:8px;padding:10px 12px;margin-bottom:10px;border-left:3px solid '+m.cb+';\">';",
        "  html+='<div style=\"font-size:14px;font-weight:bold;\">'+m.tn+'</div>';",
        "  html+='<div style=\"font-size:12px;opacity:0.75;\">Theorist: '+m.tb+'</div>';",
        "  html+='<div style=\"font-size:12px;color:#666;margin-bottom:3px;\">Conflicts: '+tag(m.bc,'conflict')+'</div>';",
        "  html+='<div style=\"font-size:12px;color:#666;\">Synergies: '+tag(m.bs,'synergy')+'</div></div>';",
        "  document.getElementById('p').innerHTML=html;",
        "}",
        "function reset(){document.getElementById('p').innerHTML='<div style=\"color:#aaa;font-size:13px;text-align:center;margin-top:50px;line-height:1.8;\">点击任意连线<br>查看两理论的关系与原因</div>';}",
        "reset();",
        "net.on('click',function(p){",
        "  if(!p.edges.length){",
        "    if(sel!==null){sel=null;edges.forEach(function(e){",
        "      var m=EM[e.id];if(!m)return;",
        "      var c=m.rt==='synergy'?'#27ae60':'#c0392b';",
        "      edges.update({id:e.id,color:{color:c,highlight:c,opacity:0.7},width:1+Math.abs(m.weight||0.5)*3});",
        "    });}",
        "    reset();return;",
        "  }",
        "  var eid=p.edges[0];var m=EM[eid];if(!m)return;",
        "  if(sel===eid){sel=null;edges.forEach(function(e){",
        "    var mm=EM[e.id];if(!mm)return;",
        "    var c=mm.rt==='synergy'?'#27ae60':'#c0392b';",
        "    edges.update({id:e.id,color:{color:c,highlight:c,opacity:0.7},width:1+Math.abs(mm.weight||0.5)*3});",
        "  });reset();return;",
        "  }",
        "  sel=eid;dimAll();hl(eid);show(eid);",
        "});",
        "})();"
    ]
    js_content = "\n".join(js_lines)

    # Assemble full HTML
    html = (
        '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n'
        '<script src="https://unpkg.com/vis-network@9.1.6/standalone/umd/vis-network.min.js"></script>\n'
        '<style>\n'
        '*{box-sizing:border-box}\n'
        'body{margin:0;padding:0;font-family:Microsoft YaHei,Arial,sans-serif;background:#f8f9fa}\n'
        '.c{display:flex;height:100vh}\n'
        '.nw{flex:1;display:flex;flex-direction:column;padding:12px;position:relative}\n'
        '#n{flex:1;border:1px solid #ddd;border-radius:10px;background:linear-gradient(135deg,#fafafa,#f0f0f0);min-height:0}\n'
        '.lf{position:absolute;bottom:14px;left:14px;background:rgba(255,255,255,0.95);padding:8px 12px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);font-size:11px;z-index:100}\n'
        '.lr{display:flex;align-items:center;margin:2px 0}\n'
        '.ll{width:22px;height:2px;margin-right:5px;border-radius:2px}\n'
        '.p{width:300px;background:white;border-left:1px solid #e0e0e0;padding:16px 14px;overflow-y:auto}\n'
        '@media(max-width:700px){.c{flex-direction:column}.p{width:100%;height:220px;border-left:none;border-top:1px solid #e0e0e0}}\n'
        '</style>\n'
        '</head>\n<body>\n'
        '<div class="c">\n'
        '<div class="nw">\n'
        '<div id="n"></div>\n'
        '<div class="lf">\n'
        '<div class="lr"><div class="ll" style="background:#27ae60;"></div><span>Green = Synergy</span></div>\n'
        '<div class="lr"><div class="ll" style="background:#c0392b;border-style:dashed;"></div><span>Red = Conflict</span></div>\n'
        '<div class="lr" style="margin-top:3px;color:#888;"><span>Click edge for details</span></div>\n'
        '</div>\n'
        '</div>\n'
        '<div class="p" id="p"></div>\n'
        '</div>\n'
        '<script>\n' + js_content + '\n</script>\n'
        '</body>\n</html>'
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path