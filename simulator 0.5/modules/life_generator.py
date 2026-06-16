"""
人生事件生成引擎 V4
彻底修复：已发生事件概率=0，严格按社会规则
集成故事逻辑验证器：FATAL问题触发重生成，安全阈值保护
"""
import yaml
import os
import random
from typing import Dict, List, Any, Optional, Set, Tuple, Callable
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
        has_unmarried = False
        has_married = False
        has_first_job = False
        has_children = False

        # 按年龄遍历 0-85岁
        for age in range(0, 86):
            current_attrs["age"] = age

            # 收集该年龄可能发生的事件
            candidates = []

            categories = ["education", "career", "family", "social", "critical", "rural_traditional", "rural_china", "mechanical_solidarity", "organic_solidarity", "metropolis", "stranger_status", "risk_society", "rationalization", "disenchantment", "field_pressure_high", "cultural_capital_high", "cultural_capital_low", "disciplinary_power", "panopticism", "modern_urban", "risk_anxiety", "digital_surveillance"]
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
                        has_primary, has_middle, has_high, has_university, has_unmarried, has_married, has_first_job
                    ):
                        continue

                    # 把category写进事件对象的副本（避免引用覆盖问题）
                    evt_copy = dict(evt)
                    evt_copy["category"] = cat

                    # 计算概率（已发生事件概率为0）
                    prob = self._calc_prob(
                        evt_copy, age, social_rules, occurred,
                        has_primary, has_middle, has_high, has_university, has_unmarried, has_married, has_first_job,
                        selected_structure_ids
                    )

                    if random.random() < prob:
                        candidates.append((eid, evt_copy))

            # 该年龄最多选择2个事件
            if candidates:
                # ---- 结构专属事件优先保障：选中某结构时，强制保证选出一个该结构事件 ----
                selected_struct = None
                for struct_id in ["rural_china", "mechanical_solidarity", "organic_solidarity", "metropolis", "stranger_status", "risk_society", "rationalization", "disenchantment", "field_pressure_high", "cultural_capital_high", "cultural_capital_low", "disciplinary_power", "panopticism"]:
                    if struct_id in selected_structure_ids:
                        struct_candidates = [c for c in candidates if c[1].get("category") == struct_id]
                        if struct_candidates:
                            selected_struct = struct_id
                            forced_event = random.choice(struct_candidates)
                            remaining = [c for c in candidates if c != forced_event]
                            if remaining:
                                second = random.sample(remaining, min(1, len(remaining)))
                                selected = (forced_event, second[0])
                            else:
                                selected = (forced_event,)
                            break
                if selected_struct is None:
                    selected = random.sample(candidates, min(2, len(candidates)))

                for eid, evt in selected:
                    event_category = evt.get("category", "unknown")
                    event = {
                        "id": eid,
                        "name": evt.get("name", "未知"),
                        "description": evt.get("description", ""),
                        "age": age,
                        "year": birth_year + age,
                        "action_emoji": "📋",
                        "sociological_reading": evt.get("sociological_reading", ""),
                        "outcomes": evt.get("outcomes", {}),
                        "category": event_category
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

        # ---- 保底机制：选中乡土社会时，至少触发一个乡土事件 ----
        if "rural_china" in selected_structure_ids:
            rural_events_in_timeline = [e for e in timeline if e.get("category") == "rural_china"]
            if not rural_events_in_timeline:
                # 强制从乡土事件库中选一个符合条件的插入
                forced_event = self._get_forced_rural_event(timeline, social_rules, occurred)
                if forced_event:
                    timeline.append(forced_event)
                    timeline.sort(key=lambda x: x["age"])

        return timeline

    def _get_forced_rural_event(
        self,
        timeline: List[Dict],
        social_rules: Dict,
        occurred: Set[str]
    ) -> Optional[Dict]:
        """当没有乡土事件时，强制获取一个可插入的乡土事件"""
        import random as rnd
        birth_year = timeline[0]["year"] - timeline[0]["age"] if timeline else 1990

        candidates: List[tuple] = []
        for evt in self.events_data.get("rural_china", {}).get("events", []):
            eid = evt.get("id", "")
            if eid in occurred:
                continue
            # 检查前置条件
            if not self._check_prerequisites(
                eid, 0, social_rules, occurred,
                False, False, False, False, False, False, False
            ):
                continue
            # 取事件定义中第一个合法年龄
            age_range = evt.get("age_range", [20, 60])
            age = rnd.randint(age_range[0], age_range[1])
            candidates.append((eid, evt, age))

        if not candidates:
            return None

        eid, evt, age = rnd.choice(candidates)
        return {
            "id": eid,
            "name": evt.get("name", "未知"),
            "description": evt.get("description", ""),
            "age": age,
            "year": birth_year + age,
            "action_emoji": "📋",
            "sociological_reading": evt.get("sociological_reading", ""),
            "outcomes": evt.get("outcomes", {}),
            "category": "rural_china"
        }

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
        has_unmarried: bool,
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

        # 乡土中国事件前置条件
        # 媒人上门说亲后才能举办婚礼
        if eid == "rural_wedding_ceremony":
            if "rural_wedding_matchmaker" not in occurred:
                return False

        # 举办婚礼后才能考虑分家析产
        if eid == "family_property_division":
            if "rural_wedding_ceremony" not in occurred:
                return False

        # 分家后长子才能当家
        if eid == "son_becomes_head":
            if "family_property_division" not in occurred:
                return False

        # 外出谋生后才能有叶落归根
        if eid == "return_to_home_village":
            if "leave_village_work" not in occurred:
                return False

        # 过继/收养需要先结婚
        if eid == "parents_arrange_adoption":
            if "rural_wedding_ceremony" not in occurred:
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
        has_university: bool,
        has_unmarried: bool,
        has_married: bool,
        has_first_job: bool,
        selected_structure_ids: List[str]
    ) -> float:
        """计算事件概率"""
        eid = evt.get("id", "")
        base = evt.get("weight", 0.5)

        # ---- 社会结构亲和性加权 ----
        # 当选中某社会结构时，提高该结构对应事件类别的概率
        cat = evt.get("category", "")
        structure_boost_map = {
            "rural_china":       "rural_china",
            "rural_traditional": "rural_china",
            "mechanical_solidarity": "mechanical_solidarity",
            "organic_solidarity":    "organic_solidarity",
            "rationalization":       "rationalization",
            "disenchantment":         "disenchantment",
            "field_pressure_high":    "field_pressure_high",
            "cultural_capital_high":  "cultural_capital_high",
            "cultural_capital_low":   "cultural_capital_low",
            "disciplinary_power":    "disciplinary_power",
            "panopticism":            "panopticism",
            "rural_china":            "rural_china",
            "metropolis":             "metropolis",
            "stranger_status":        "stranger_status",
            "risk_society":            "risk_society",
        }
        boost_key = structure_boost_map.get(cat, cat)
        if boost_key in selected_structure_ids:
            base *= 3.5   # 选中对应结构时，该类事件概率提升3.5倍
        elif cat in structure_boost_map.values():
            # 该类别是结构专属事件，但选中结构列表中不含对应结构 → 概率归零，完全排除
            return 0.0

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

        # ---- 乡土中国事件的特殊概率 ----
        # 做三朝/满月酒：只能在婴儿1岁前发生
        if eid == "rural_birth_feast":
            if age == 0:
                return base * 0.9
            return 0.0

        # 媒人上门说亲 → 婚礼：必须先媒人说亲才能办婚礼
        if eid == "rural_wedding_ceremony":
            if "rural_wedding_matchmaker" in occurred:
                if 16 <= age <= 28:
                    return base * 0.9
            return 0.0

        if eid == "rural_wedding_matchmaker":
            if "rural_wedding_ceremony" in occurred:
                return 0.0  # 婚礼已办过不再重复说亲

        # 分家析产后才轮到长子当家
        if eid == "son_becomes_head":
            if "family_property_division" not in occurred:
                return 0.0
            if 50 <= age <= 70:
                return base * 0.6
            return 0.0

        # 购置田地与卖地互斥（买了不再卖地，或卖了可再买）
        if eid == "land_purchase":
            if age < 25 or age > 50:
                return 0.0
            return base * 0.4

        if eid == "land_sale_under_pressure":
            if age < 25 or age > 60:
                return 0.0
            return base * 0.3

        # 叶落归根：必须先外出谋生才能回乡
        if eid == "return_to_home_village":
            if "leave_village_work" not in occurred:
                return 0.0
            if 45 <= age <= 75:
                return base * 0.5
            return 0.0

        # 外出谋生：年纪大了不再外出
        if eid == "leave_village_work":
            if age < 16 or age > 30:
                return 0.0
            return base * 0.35

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
        """生成带可视化的时间线（带故事逻辑验证）"""
        from .story_validator import StoryValidator

        validator = StoryValidator()

        # 包装生成函数
        def generate_fn(char, struct_ids, s):
            return self.generate_life_timeline(char, struct_ids, s)

        # 带重试的生成
        timeline, validation_result = validator.validate_with_retry(
            generate_fn=generate_fn,
            character=character,
            selected_structure_ids=selected_structure_ids,
            initial_seed=seed
        )

        return {
            "timeline": timeline,
            "metadata": {
                "total": len(timeline),
                "validation": {
                    "passed": validation_result.passed,
                    "fatal": validation_result.fatal_count,
                    "serious": validation_result.serious_count,
                    "minor": validation_result.minor_count,
                    "retries": validation_result.retry_count,
                    "report": validation_result.report()
                }
            }
        }