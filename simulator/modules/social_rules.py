"""
社会规则引擎 - 根据选中的社会结构生成该社会的规则
"""
import yaml
import os
from typing import Dict, List, Any, Optional


class SocialRulesEngine:
    """根据社会结构生成社会规则"""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir
        self._load_rules()

    def _load_rules(self):
        """加载社会规则"""
        rules_path = os.path.join(self.data_dir, "social_rules.yaml")
        with open(rules_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.default_rules = data["social_rules"]["default"]
        self.structure_modifiers = data.get("structure_modifiers", {})

    def generate_social_rules(
        self,
        selected_structure_ids: List[str]
    ) -> Dict[str, Any]:
        """
        根据选中的社会结构生成该社会的完整规则

        Returns:
            社会规则字典
        """
        # 从默认规则开始
        rules = {
            "name": "混合现代社会",
            "education": self.default_rules["education"].copy(),
            "work": self.default_rules["work"].copy(),
            "marriage": self.default_rules["marriage"].copy(),
            "social": self.default_rules["social"].copy(),
            "features": []
        }

        # 收集各维度的modifier
        education_mods = []
        work_mods = []
        marriage_mods = []
        social_mods = []

        for struct_id in selected_structure_ids:
            if struct_id in self.structure_modifiers:
                mod = self.structure_modifiers[struct_id]
                rules["name"] = mod.get("name", rules["name"])

                if "education" in mod:
                    education_mods.append(mod["education"])
                if "work" in mod:
                    work_mods.append(mod["work"])
                if "marriage" in mod:
                    marriage_mods.append(mod["marriage"])
                if "social" in mod:
                    social_mods.append(mod["social"])

        # 合并规则（取极端值或平均值）
        if education_mods:
            rules["education"] = self._merge_dicts(
                rules["education"], education_mods[-1]
            )
        if work_mods:
            rules["work"] = self._merge_dicts(rules["work"], work_mods[-1])
        if marriage_mods:
            rules["marriage"] = self._merge_dicts(rules["marriage"], marriage_mods[-1])
        if social_mods:
            rules["social"] = self._merge_dicts(rules["social"], social_mods[-1])

        # 生成规则描述
        rules["description"] = self._generate_description(rules)

        return rules

    def _merge_dicts(self, base: Dict, override: Dict) -> Dict:
        """合并字典，override覆盖base"""
        result = base.copy()
        for k, v in override.items():
            if isinstance(v, dict):
                result[k] = self._merge_dicts(result.get(k, {}), v)
            else:
                result[k] = v
        return result

    def _generate_description(self, rules: Dict[str, Any]) -> str:
        """生成规则描述文本"""
        lines = []
        edu = rules["education"]
        work = rules["work"]
        mar = rules["marriage"]
        soc = rules["social"]

        lines.append(f"**义务教育**：{edu['compulsory_years']}年（{edu['school_start_age']}岁入学）")

        # 计算各教育阶段毕业年龄
        primary_end = edu['school_start_age'] + edu['primary_years']
        middle_end = primary_end + edu.get('middle_years', 3)
        high_end = middle_end + edu.get('high_years', 3)
        university_end = high_end + edu.get('university_years', 4)

        lines.append(f"**教育路径**：{edu['school_start_age']}岁小学→{primary_end}岁毕业→{middle_end}岁初中→{high_end}岁高中→{university_end}岁大学")

        lines.append(f"**工作年龄**：{work['min_age']}岁可工作，典型首份工作{work['typical_first_job']}岁，法定退休{work['retirement_age']}岁")

        lines.append(f"**婚姻制度**：法定婚龄{mar['legal_age']}岁，包办婚姻比例{int(mar['arranged_ratio']*100)}%")

        mobility_desc = "高" if soc.get('class_mobility', 0.3) > 0.4 else "低"
        lines.append(f"**社会流动**：阶层流动性{mobility_desc}")

        urban_desc = "自由" if soc.get('urban_freedom', 0.5) > 0.5 else "受限"
        lines.append(f"**城乡流动**：{urban_desc}")

        return "\n".join(lines)

    def get_education_timeline(self, rules: Dict[str, Any]) -> Dict[int, str]:
        """获取教育时间线（年龄->教育阶段）"""
        edu = rules["education"]
        start = edu["school_start_age"]
        timeline = {}

        timeline[start] = "进入小学"
        timeline[start + edu["primary_years"]] = "小学毕业"

        middle_years = edu.get("middle_years", 3)
        if middle_years > 0:
            timeline[start + edu["primary_years"] + middle_years] = "初中毕业"

        high_years = edu.get("high_years", 3)
        if high_years > 0:
            timeline[start + edu["primary_years"] + middle_years + high_years] = "高中毕业"

        university_years = edu.get("university_years", 4)
        if university_years > 0:
            timeline[start + edu["primary_years"] + middle_years + high_years + university_years] = "大学毕业"

        return timeline

    def calculate_retirement_age(self, rules: Dict[str, Any]) -> int:
        """计算退休年龄"""
        return rules["work"].get("retirement_age", 60)