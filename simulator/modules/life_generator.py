"""
人生事件生成引擎 V4
彻底修复：已发生事件概率=0，严格按社会规则
"""
import yaml
import os
import random
from typing import Dict, List, Any, Optional, Set
from .structure_engine import StructureEngine
from .character_gen import CharacterGenerator
from .social_rules import SocialRulesEngine


class LifeGenerator:
    """人生事件生成引擎 V4"""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir
        self.events_data = self._load_events()
        self.structure_engine = StructureEngine(data_dir)
        self.character_gen = CharacterGenerator(data_dir)
        self.social_rules_engine = SocialRulesEngine(data_dir)

    def _load_events(self) -> Dict[str, Any]:
        events_path = os.path.join(self.data_dir, "events.yaml")
        with open(events_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data["life_events"]

    def generate_life_timeline(
        self,
        character: Dict[str, Any],
        selected_structure_ids: List[str],
        seed: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """生成人生时间线"""
        if seed is not None:
            random.seed(seed)

        timeline = []
        current_attrs = character["attributes"].copy()
        birth_year = character["birth_year"]

        # 生成社会规则
        social_rules = self.social_rules_engine.generate_social_rules(selected_structure_ids)

        # 已发生事件ID集合
        occurred: Set[str] = set()

        # 跟踪教育进度（通过已发生事件判断）
        has_primary = False
        has_middle = False
        has_high = False
        has_university = False
        has_married = False
        has_first_job = False
        has_children = False

        # 按年龄遍历 0-85岁
        for age in range(0, 86):
            current_attrs["age"] = age

            # 收集该年龄可能发生的事件
            candidates = []

            categories = ["education", "career", "family", "social", "critical", "rural_traditional", "modern_urban", "disciplinary_high_control", "risk_anxiety", "digital_surveillance"]
            for cat in categories:
                if cat not in self.events_data:
                    continue
                for evt in self.events_data[cat].get("events", []):
                    eid = evt.get("id", "")

                    # 跳过已发生事件
                    if eid in occurred:
                        continue

                    # 检查年龄范围
                    age_range = evt.get("age_range", [0, 100])
                    if not (age_range[0] <= age <= age_range[1]):
                        continue

                    # 检查前置条件
                    if not self._check_prerequisites(
                        eid, age, social_rules, occurred,
                        has_primary, has_middle, has_high, has_university, has_married, has_first_job
                    ):
                        continue

                    # 计算概率（已发生事件概率为0）
                    prob = self._calc_prob(
                        evt, age, social_rules, occurred,
                        has_primary, has_middle, has_high, has_university, has_married, has_first_job
                    )

                    if random.random() < prob:
                        candidates.append((eid, evt))

            # 该年龄最多选择2个事件
            if candidates:
                selected = random.sample(candidates, min(2, len(candidates)))
                for eid, evt in selected:
                    event = {
                        "id": eid,
                        "name": evt.get("name", "未知"),
                        "description": evt.get("description", ""),
                        "age": age,
                        "year": birth_year + age,
                        "action_emoji": "📋",
                        "sociological_reading": evt.get("sociological_reading", ""),
                        "outcomes": evt.get("outcomes", {}),
                        "category": cat
                    }
                    timeline.append(event)
                    occurred.add(eid)

                    # 更新属性
                    if "outcomes" in evt:
                        current_attrs = self._apply_outcomes(current_attrs, evt["outcomes"])

                    # 更新教育/婚姻/工作进度
                    if eid == "enter_primary_school":
                        has_primary = True
                    elif eid == "enter_middle_school":
                        has_middle = True
                    elif eid == "enter_high_school":
                        has_high = True
                    elif eid == "college_enrollment":
                        has_university = True
                    elif eid in ["marriage", "arranged_marriage"]:
                        has_married = True
                    elif eid in ["first_job", "first_internship"]:
                        has_first_job = True
                    elif eid in ["first_child_born", "second_child_born"]:
                        has_children = True

        # 按年龄排序
        timeline.sort(key=lambda x: x["age"])
        return timeline

    def _check_prerequisites(
        self,
        eid: str,
        age: int,
        social_rules: Dict,
        occurred: Set[str],
        has_primary: bool,
        has_middle: bool,
        has_high: bool,
        has_university: bool,
        has_married: bool,
        has_first_job: bool
    ) -> bool:
        """检查前置条件"""
        edu = social_rules.get("education", {})
        work = social_rules.get("work", {})
        marriage = social_rules.get("marriage", {})

        # 教育事件前置
        education_chain = {
            "enter_middle_school": has_primary,
            "middle_school_graduation": has_middle,
            "enter_high_school": has_middle,  # 如果middle_years=0，则初中毕业=小学毕业
            "high_school_graduation": has_high,
            "take_college_entrance_exam": has_high,
            "college_enrollment": has_high,  # 高考后录取
            "college_graduation": has_university,
            "enter_graduate_school": has_university,
        }

        if eid in education_chain:
            if not education_chain[eid]:
                return False

        # 高考必须先完成高中
        if eid == "take_college_entrance_exam" and not has_high:
            return False

        # 大学入学必须先参加高考
        if eid == "college_enrollment" and not has_high:
            return False

        # 婚姻事件
        if eid in ["marriage", "arranged_marriage"]:
            legal_age = marriage.get("legal_age", 22)
            if age < legal_age:
                return False

        # 子女事件需要先结婚
        if eid in ["first_child_born", "second_child_born"]:
            if not has_married:
                return False
            legal_age = marriage.get("legal_age", 22)
            if age < legal_age + 2:
                return False

        # 工作事件
        if eid in ["first_job", "first_internship"]:
            min_age = work.get("min_age", 16)
            if age < min_age:
                return False

        # 退休事件
        if eid == "retirement":
            retirement_age = work.get("retirement_age", 60)
            if age < retirement_age:
                return False

        # 同居需要先谈恋爱
        if eid == "cohabitation":
            if "falling_in_love" not in occurred and "first_love" not in occurred:
                return False

        # 孩子上学需要先生育
        if eid == "child_start_school":
            if "first_child_born" not in occurred:
                return False
            # 孩子通常6-7岁上学
            if age < 30:  # 假设30岁前有孩子，上学年龄30+
                return False

        # 孩子高考需要孩子先上学
        if eid == "child_college_entrance":
            if "child_start_school" not in occurred:
                return False

        # 子女离家需要先生育，且子女已长大
        if eid == "children_leave_home":
            if "first_child_born" not in occurred:
                return False
            # 子女通常18-25岁离家
            if age < 45:
                return False

        # 父母去世通常在50岁之后
        if eid == "parents_pass_away":
            if age < 45:
                return False

        # 退休后再就业需要先退休
        if eid == "reemployment_after_retirement":
            if "retirement" not in occurred:
                return False

        return True

    def _calc_prob(
        self,
        evt: Dict,
        age: int,
        social_rules: Dict,
        occurred: Set[str],
        has_primary: bool,
        has_middle: bool,
        has_high: bool,
        has_unmarried: bool,
        has_married: bool,
        has_first_job: bool
    ) -> float:
        """计算事件概率"""
        eid = evt.get("id", "")
        base = evt.get("weight", 0.5)

        edu = social_rules.get("education", {})
        work = social_rules.get("work", {})
        marriage = social_rules.get("marriage", {})

        # 已发生事件概率为0
        if eid in occurred:
            return 0.0

        # 小学入学：8岁（乡土社会）
        if eid == "enter_primary_school":
            school_start = edu.get("school_start_age", 6)
            if age == school_start:
                return base * 0.95
            elif age < school_start:
                return 0.0
            else:
                return base * 0.05  # 延迟入学

        # 小学毕业
        if eid == "primary_school_graduation":
            school_start = edu.get("school_start_age", 6)
            primary_years = edu.get("primary_years", 6)
            grad_age = school_start + primary_years
            if age == grad_age:
                return base * 0.95
            elif age < grad_age:
                return 0.0
            else:
                return base * 0.02

        # 进入初中（如果没有初中阶段，则跳过）
        if eid == "enter_middle_school":
            middle_years = edu.get("middle_years", 3)
            if middle_years == 0:
                return 0.0  # 没有初中阶段
            school_start = edu.get("school_start_age", 6)
            primary_years = edu.get("primary_years", 6)
            enter_age = school_start + primary_years
            if age == enter_age:
                return base * 0.95
            elif age < enter_age:
                return 0.0
            else:
                return base * 0.02

        # 初中毕业
        if eid == "middle_school_graduation":
            middle_years = edu.get("middle_years", 3)
            if middle_years == 0:
                return 0.0
            school_start = edu.get("school_start_age", 6)
            primary = edu.get("primary_years", 6)
            grad_age = school_start + primary + middle_years
            if age == grad_age:
                return base * 0.95
            elif age < grad_age:
                return 0.0
            else:
                return base * 0.02

        # 进入高中
        if eid == "enter_high_school":
            middle_years = edu.get("middle_years", 3)
            school_start = edu.get("school_start_age", 6)
            primary = edu.get("primary_years", 6)
            enter_age = school_start + primary + middle_years
            if age == enter_age:
                return base * 0.9
            elif age < enter_age:
                return 0.0
            else:
                return base * 0.02

        # 高中毕业/高考
        if eid in ["high_school_graduation", "take_college_entrance_exam"]:
            middle = edu.get("middle_years", 3)
            high = edu.get("high_years", 3)
            school_start = edu.get("school_start_age", 6)
            grad_age = school_start + edu.get("primary_years", 6) + middle + high
            if age == grad_age:
                return base * 0.95
            elif age < grad_age:
                return 0.0
            else:
                return base * 0.02

        # 大学录取
        if eid == "college_enrollment":
            middle = edu.get("middle_years", 3)
            high = edu.get("high_years", 3)
            school_start = edu.get("school_start_age", 6)
            entrance_age = school_start + edu.get("primary_years", 6) + middle + high
            if age == entrance_age:
                return base * 0.7
            elif age < entrance_age:
                return 0.0
            else:
                return base * 0.02

        # 大学入学后毕业
        if eid == "college_graduation":
            if not has_university:
                return 0.0
            university_years = edu.get("university_years", 4)
            middle = edu.get("middle_years", 3)
            high = edu.get("high_years", 3)
            school_start = edu.get("school_start_age", 6)
            grad_age = school_start + edu.get("primary_years", 6) + middle + high + university_years
            if age == grad_age:
                return base * 0.95
            elif age < grad_age:
                return 0.0
            else:
                return base * 0.02

        # 第一份工作
        if eid in ["first_job", "first_internship"]:
            typical = work.get("typical_first_job", 18)
            min_age = work.get("min_age", 16)
            if age >= min_age:
                if age == typical:
                    return base * 0.8
                elif age > typical:
                    return base * 0.2
                else:
                    return base * 0.05
            return 0.0

        # 退休
        if eid == "retirement":
            ret_age = work.get("retirement_age", 60)
            if age == ret_age:
                return base * 0.9
            elif age < ret_age:
                return 0.0
            else:
                return base * 0.3

        # 婚姻
        if eid in ["marriage", "arranged_marriage"]:
            legal = marriage.get("legal_age", 22)
            if age >= legal:
                if age <= legal + 5:
                    return base * 0.4
                elif age <= legal + 15:
                    return base * 0.2
                else:
                    return base * 0.05
            return 0.0

        # 子女出生
        if eid in ["first_child_born", "second_child_born"]:
            legal = marriage.get("legal_age", 22)
            if age >= legal + 2 and age <= legal + 15:
                return base * 0.3
            elif age > legal + 15:
                return base * 0.05
            return 0.0

        # 孩子上学需要先有孩子
        if eid == "child_start_school":
            if "first_child_born" not in occurred:
                return 0.0
            # 孩子6-7岁上学，所以父母通常30-35岁
            if 30 <= age <= 40:
                return base * 0.5
            return 0.0

        # 子女离家
        if eid == "children_leave_home":
            if "first_child_born" not in occurred:
                return 0.0
            # 子女18-25岁离家
            if age >= 45:
                return base * 0.3
            return 0.0

        # 默认概率（降低整体概率，减少事件数量）
        return base * 0.15

    def _apply_outcomes(
        self,
        attrs: Dict[str, float],
        outcomes: Dict[str, tuple]
    ) -> Dict[str, float]:
        """应用事件结果"""
        new_attrs = attrs.copy()
        for attr, change_range in outcomes.items():
            min_c, max_c = change_range
            change = random.uniform(min_c, max_c)
            if attr == "education_level":
                new_attrs[attr] = max(0.0, min(7.0, new_attrs.get(attr, 0.0) + change))
            elif attr in ["stress_level", "anomie_level", "field_pressure",
                          "surveillance_level", "social_isolation"]:
                new_attrs[attr] = max(0.0, min(1.0, new_attrs.get(attr, 0.0) + change))
            else:
                new_attrs[attr] = max(-1.0, min(1.0, new_attrs.get(attr, 0.0) + change))
        return new_attrs

    def generate_timeline_with_visualization(
        self,
        character: Dict[str, Any],
        selected_structure_ids: List[str],
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """生成带可视化的时间线"""
        timeline = self.generate_life_timeline(
            character, selected_structure_ids, seed
        )
        return {
            "timeline": timeline,
            "metadata": {"total": len(timeline)}
        }