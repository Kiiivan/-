"""
人物生成器
根据玩家设定生成虚拟人物，初始化其属性向量
"""
import yaml
import os
from typing import Dict, List, Any, Optional
import random


class CharacterGenerator:
    """人物属性生成器"""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir
        self.templates = self._load_templates()
        self.places = self._load_places()

    def _load_templates(self) -> Dict[str, Any]:
        """加载人物模板"""
        templates_path = os.path.join(self.data_dir, "character_templates.yaml")
        with open(templates_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data["character_templates"]

    def _load_places(self) -> Dict[str, Any]:
        """加载出生地数据"""
        places_path = os.path.join(self.data_dir, "places.yaml")
        with open(places_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data["places"]

    def get_gender_options(self) -> List[Dict[str, Any]]:
        """获取性别选项"""
        return self.templates.get("gender", [])

    def get_birth_place_options(self) -> List[Dict[str, Any]]:
        """获取出生地选项"""
        return self.templates.get("birth_place", [])

    def get_era_options(self) -> List[Dict[str, Any]]:
        """获取时代选项"""
        return self.templates.get("era", [])

    def get_parent_class_options(self) -> List[Dict[str, Any]]:
        """获取父母阶层选项"""
        return self.templates.get("parent_class", [])

    def get_preset_characters(self) -> List[Dict[str, Any]]:
        """获取预设人物列表"""
        return self.templates.get("preset_characters", [])

    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """获取出生地详细信息"""
        # 先检查是否是城市
        for city in self.places.get("cities", []):
            if city["id"] == place_id:
                return city
        # 检查是否是城镇
        for town in self.places.get("towns", []):
            if town["id"] == place_id:
                return town
        # 检查是否是农村
        for village in self.places.get("rural_areas", []):
            if village["id"] == place_id:
                return village
        return None

    def generate_character(
        self,
        gender_id: Optional[str] = None,
        birth_place_id: Optional[str] = None,
        era_id: Optional[str] = None,
        parent_class_id: Optional[str] = None,
        preset_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        根据设定生成人物

        Args:
            gender_id: 性别ID
            birth_place_id: 出生地ID
            era_id: 时代ID
            parent_class_id: 父母阶层ID
            preset_id: 预设人物ID（如果使用预设，则忽略其他参数）

        Returns:
            人物对象
        """
        character = {
            "name": self._generate_name(gender_id),
            "gender": gender_id or "male",
            "birth_place": birth_place_id or "small_town",
            "era": era_id or "reform_late",
            "parent_class": parent_class_id or "white_collar",
            "attributes": {},
            "birth_year": self._estimate_birth_year(era_id),
            "life_events": []
        }

        # 初始化属性
        attributes = self._initialize_attributes(character)
        character["attributes"] = attributes

        return character

    def _generate_name(self, gender_id: Optional[str]) -> str:
        """生成随机姓名"""
        surnames = ["李", "王", "张", "刘", "陈", "杨", "黄", "赵", "周", "吴",
                    "徐", "孙", "马", "朱", "胡", "郭", "林", "何", "高", "梁"]
        given_names_male = ["伟", "强", "磊", "洋", "勇", "军", "杰", "涛", "明", "超",
                           "辉", "鹏", "飞", "文", "博", "浩", "宇", "浩", "志", "明"]
        given_names_female = ["芳", "娟", "敏", "静", "丽", "艳", "娜", "秀", "英", "华",
                              "婷", "玉", "梅", "兰", "云", "莲", "珍", "凤", "洁", "慧"]

        surname = random.choice(surnames)
        if gender_id == "female":
            given_name = random.choice(given_names_female)
        else:
            given_name = random.choice(given_names_male)

        return f"{surname}{given_name}"

    def _estimate_birth_year(self, era_id: Optional[str]) -> int:
        """估算出生年份"""
        if era_id:
            era = self._find_era(era_id)
            if era:
                year_range = era.get("year_range", [1990, 2000])
                return (year_range[0] + year_range[1]) // 2
        return 1995

    def _find_era(self, era_id: str) -> Optional[Dict[str, Any]]:
        """查找时代信息"""
        for era in self.templates.get("era", []):
            if era["id"] == era_id:
                return era
        return None

    def _initialize_attributes(
        self,
        character: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        初始化人物属性

        属性说明：
        - education_level: 教育水平 (0-5, 对应：文盲/扫盲、小学、初中、高中/职高、大专/本科、研究生)
        - cultural_capital: 文化资本 (-1.0 到 1.0)
        - economic_capital: 经济资本 (-1.0 到 1.0)
        - social_capital: 社会资本 (-1.0 到 1.0)
        - anomie_level: 失范水平 (0.0 到 1.0)
        - stress_level: 压力水平 (0.0 到 1.0)
        - social_mobility: 社会流动性 (-1.0 到 1.0)
        - field_pressure: 场域压力 (0.0 到 1.0)
        - impression_management: 印象管理水平 (0.0 到 1.0)
        - stranger_status: 陌生人处境 (0.0 到 1.0)
        - surveillance_level: 监视水平 (0.0 到 1.0)
        - community_integration: 社区整合度 (0.0 到 1.0)
        - face_consciousness: 面子意识 (0.0 到 1.0)
        - guanxi_dependence: 关系依赖度 (0.0 到 1.0)
        - traditional_action_weight: 传统行动权重 (0.0 到 1.0)
        - instrumental_rational_weight: 工具理性行动权重 (0.0 到 1.0)
        - value_rational_weight: 价值理性行动权重 (0.0 到 1.0)
        - affective_action_weight: 情感行动权重 (0.0 到 1.0)
        """
        attrs = {
            "education_level": 0.0,
            "cultural_capital": 0.0,
            "economic_capital": 0.0,
            "social_capital": 0.0,
            "anomie_level": 0.0,
            "stress_level": 0.0,
            "social_mobility": 0.0,
            "field_pressure": 0.0,
            "impression_management": 0.0,
            "stranger_status": 0.0,
            "surveillance_level": 0.0,
            "community_integration": 0.0,
            "face_consciousness": 0.0,
            "guanxi_dependence": 0.0,
            "traditional_action_weight": 0.2,
            "instrumental_rational_weight": 0.2,
            "value_rational_weight": 0.2,
            "affective_action_weight": 0.2,
            # Additional attributes needed for trigger conditions
            "education_opportunity": 0.3,
            "field_pressure_high": 0.0,
            "urban_area": 0.0,
            "marriage": 0.0,
            "impression_management_society": 0.0,
            "sociological_imagination": 0.0,
            "critical_awareness": 0.0,
            "risk_exposure": 0.0,
            "risk_society": 0.0,
            "urbanization": 0.0,
            "individualization": 0.0,
            "mechanical_solidarity": 0.0,
            "organic_solidarity": 0.0,
            "ritual_order": 0.0,
            "rule_of_law": 0.0,
            "differential_associate_pattern": 0.0,
            "digital_surveillance": 0.0,
            "rationalization": 0.0,
            "disenchantment": 0.0,
            "metropolis": 0.0,
            "money_culture": 0.0,
            "blasé_attitude": 0.0,
            "objectification": 0.0,
            "individual_freedom": 0.0,
            "traditional_values": 0.0,
            "emotional_stability": 0.5,
            "information_overload": 0.0,
            "population_management": 0.0,
            "health_level": 0.5,
            "national_identity": 0.0,
            "media_consumption": 0.0,
            "political_participation": 0.0,
            "front_stage_performance": 0.0,
            "authentic_self": 0.5,
            "social_competence": 0.3,
            "legal_system_importance": 0.0,
            "conflict_resolution_formal": 0.0,
            "traditional_norm_compliance": 0.0,
            "reflexive_modernization": 0.0,
            "institutional_trust": 0.5,
            "market_oriented": 0.0,
            "petit_bourgeois": 0.0,
            "bureaucracy_level": 0.0,
            "field_pressure_resistance": 0.0,
            "class_background": 0.0,
            "habitus_guided_action": 0.0,
            "capital_competition": 0.0,
        }

        # 应用出生地修饰符
        birth_place = self._find_birth_place(character["birth_place"])
        if birth_place:
            for attr, change in birth_place.items():
                if attr in attrs and isinstance(change, (int, float)):
                    attrs[attr] = max(-1.0, min(1.0, attrs.get(attr, 0.0) + change))

        # 应用时代修饰符
        era = self._find_era(character["era"])
        if era:
            for attr, change in era.items():
                if attr in attrs and isinstance(change, (int, float)):
                    attrs[attr] = max(-1.0, min(1.0, attrs.get(attr, 0.0) + change))

        # 应用父母阶层修饰符
        parent_class = self._find_parent_class(character["parent_class"])
        if parent_class:
            for attr, change in parent_class.items():
                if attr in attrs and isinstance(change, (int, float)):
                    attrs[attr] = max(-1.0, min(1.0, attrs.get(attr, 0.0) + change))

        # 应用性别修饰符
        gender = self._find_gender(character["gender"])
        if gender:
            for attr, change in gender.items():
                if attr in attrs and isinstance(change, (int, float)):
                    attrs[attr] = max(-1.0, min(1.0, attrs.get(attr, 0.0) + change))

        return attrs

    def _find_birth_place(self, place_id: str) -> Optional[Dict[str, float]]:
        """查找出生地修饰符"""
        for bp in self.templates.get("birth_place", []):
            if bp["id"] == place_id:
                return bp.get("starting_modifiers", {})
        return None

    def _find_parent_class(self, class_id: str) -> Optional[Dict[str, float]]:
        """查找父母阶层修饰符"""
        for pc in self.templates.get("parent_class", []):
            if pc["id"] == class_id:
                return pc.get("starting_modifiers", {})
        return None

    def _find_gender(self, gender_id: str) -> Optional[Dict[str, float]]:
        """查找性别修饰符"""
        for g in self.templates.get("gender", []):
            if g["id"] == gender_id:
                return g.get("starting_modifiers", {})
        return None

    def apply_preset(self, preset_id: str) -> Optional[Dict[str, Any]]:
        """应用预设人物模板"""
        for preset in self.templates.get("preset_characters", []):
            if preset["id"] == preset_id:
                character = {
                    "name": self._generate_name(preset.get("gender")),
                    "gender": preset.get("gender", "male"),
                    "birth_place": preset.get("birth_place", "small_town"),
                    "era": preset.get("era", "reform_late"),
                    "parent_class": preset.get("parent_class", "white_collar"),
                    "attributes": preset.get("starting_attributes", {}).copy(),
                    "birth_year": self._estimate_birth_year(preset.get("era")),
                    "life_events": [],
                    "preset_origin": preset["id"]
                }
                return character
        return None

    def get_character_summary(self, character: Dict[str, Any]) -> str:
        """生成人物简介文本"""
        gender = self._find_gender(character["gender"])
        birth_place = self._find_birth_place(character["birth_place"])
        era = self._find_era(character["era"])
        parent_class = self._find_parent_class(character["parent_class"])

        lines = [
            f"## 👤 {character['name']}\n",
            f"**基本信息**：",
            f"- 性别：{gender.get('name', '未知') if gender else '未知'}",
            f"- 出生地：{birth_place.get('name', '未知') if birth_place else '未知'}",
            f"- 时代：{era.get('name', '未知') if era else '未知'}",
            f"- 父母阶层：{parent_class.get('name', '未知') if parent_class else '未知'}",
            f"- 出生年份：约{character['birth_year']}年",
            ""
        ]

        return "\n".join(lines)


if __name__ == "__main__":
    # 测试代码
    gen = CharacterGenerator()
    print("预设人物：")
    for p in gen.get_preset_characters():
        print(f"  {p['emoji']} {p['name']}: {p['description']}")