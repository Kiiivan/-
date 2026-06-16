"""
故事逻辑检测器模块
=================

集成 universal_story_validator 的核心检测逻辑，
对生成的人生故事进行逻辑性检测，不通过则重新生成。

阈值策略：
  - FATAL 数量 > 0 → 必须重试
  - SERIOUS 数量 > 3 → 建议重试
  - 达到最大重试次数后停止，以最后生成的结果输出
"""

import copy
import random
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import date
from enum import Enum


# =====================================================================
# 基础数据结构（从 universal_story_validator 精简）
# =====================================================================

class Severity(Enum):
    FATAL = "FATAL"
    SERIOUS = "SERIOUS"
    MINOR = "MINOR"


@dataclass
class Issue:
    code: str
    severity: Severity
    message: str
    event_index: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """检测结果封装"""
    issues: List[Issue] = field(default_factory=list)
    passed: bool = True
    fatal_count: int = 0
    serious_count: int = 0
    minor_count: int = 0
    retry_count: int = 0

    @classmethod
    def from_issues(cls, issues: List[Issue], retry_count: int = 0) -> "ValidationResult":
        fatal = sum(1 for i in issues if i.severity == Severity.FATAL)
        serious = sum(1 for i in issues if i.severity == Severity.SERIOUS)
        minor = sum(1 for i in issues if i.severity == Severity.MINOR)
        return cls(
            issues=issues,
            passed=fatal == 0,
            fatal_count=fatal,
            serious_count=serious,
            minor_count=minor,
            retry_count=retry_count
        )

    def report(self) -> str:
        lines = [
            "=" * 50,
            f"故事逻辑检测报告（重试次数：{self.retry_count}）",
            "=" * 50,
            f"FATAL: {self.fatal_count}  SERIOUS: {self.serious_count}  MINOR: {self.minor_count}",
            f"判定：{'✅ 通过' if self.passed else '❌ 不通过'}",
            "",
        ]
        if self.issues:
            for issue in self.issues[:10]:  # 最多显示10条
                tag = {"FATAL": "🔴", "SERIOUS": "🟡", "MINOR": "🟢"}[issue.severity.value]
                loc = f"[事件{issue.event_index}]" if issue.event_index is not None else ""
                lines.append(f"  {tag} {issue.code} {loc} {issue.message}")
                if issue.suggestion:
                    lines.append(f"     └─ {issue.suggestion}")
            if len(self.issues) > 10:
                lines.append(f"  ... 还有 {len(self.issues) - 10} 条问题")
        return "\n".join(lines)


# =====================================================================
# 时间线 → Validator 数据模型转换
# =====================================================================

@dataclass
class ValidatorCharacter:
    """适配 Validator 的人物格式"""
    id: str
    name: str
    birth_year: int
    death_year: Optional[int] = None
    gender: str = ""
    attributes: Dict[str, float] = field(default_factory=dict)
    skills: List[str] = field(default_factory=list)


@dataclass
class ValidatorEvent:
    """适配 Validator 的事件格式"""
    index: int
    year: int
    age: int
    character_id: str
    event_type: str
    description: str = ""
    causes: List[int] = field(default_factory=list)
    attribute_changes: Dict[str, float] = field(default_factory=dict)
    location: str = ""
    tags: List[str] = field(default_factory=list)
    involved_characters: List[str] = field(default_factory=list)
    skill_required: List[str] = field(default_factory=list)


def timeline_to_validator_format(
    timeline: List[Dict[str, Any]],
    character: Dict[str, Any]
) -> Tuple[ValidatorCharacter, List[ValidatorEvent]]:
    """将模拟器的时间线格式转换为 Validator 需要的格式"""
    char_id = f"char_{character.get('name', 'main').replace(' ', '_')}"

    vchar = ValidatorCharacter(
        id=char_id,
        name=character.get("name", "未知人物"),
        birth_year=character.get("birth_year", 1970),
        death_year=character.get("death_year"),
        gender=character.get("gender", ""),
        attributes=character.get("attributes", {}),
        skills=character.get("skills", [])
    )

    v_events = []
    for i, evt in enumerate(timeline):
        v_evt = ValidatorEvent(
            index=i,
            year=evt.get("year", 1970 + evt.get("age", 0)),
            age=evt.get("age", 0),
            character_id=char_id,
            event_type=evt.get("name", evt.get("id", "")),
            description=evt.get("description", ""),
            attribute_changes=evt.get("outcomes", {}),
            location=evt.get("location", ""),
        )
        v_events.append(v_evt)

    return vchar, v_events


# =====================================================================
# 核心检测逻辑（精简自 universal_story_validator，保留最关键检测）
# =====================================================================

class LogicValidator:
    """逻辑一致性检测"""

    CAUSE_WEIGHT = {
        "死亡": 5, "重病": 4, "重伤": 4, "天灾": 4, "战争": 5,
        "失业": 3, "离婚": 3, "结婚": 3, "生子": 3,
        "获奖": 2, "升职": 2, "批评": 1, "日常": 1,
    }
    EFFECT_WEIGHT = {
        "改变职业": 4, "迁移": 4, "自杀": 5,
        "信仰转变": 3, "经济变化": 3, "性格改变": 4,
        "离婚": 3, "结婚": 3, "日常": 1, "情绪": 1,
    }
    LOW_PROB = {"遗产": 0.01, "中奖": 0.001, "创业成功": 0.03, "被贵人看中": 0.02}

    def check(self, events: List[ValidatorEvent], birth_year: int) -> List[Issue]:
        issues = []
        issues.extend(self._check_timeline(events))
        issues.extend(self._check_causal_adequacy(events))
        issues.extend(self._check_event_gaps(events, birth_year))
        return issues

    def _check_timeline(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        # 识别本人死亡的事件（排除他人死亡、隐喻性死亡）
        # 排除的情况：
        # 1. 他人死亡（父母去世、亲人去世等）
        # 2. 隐喻性死亡（社会性死亡、羞耻的死亡等）
        DEATH_EXCLUDE_KW = {
            "父母", "父亲", "母亲", "亲人", "配偶", "子女", "老人", "爷爷", "奶奶",
            "外公", "外婆", "丈夫", "妻子", "爱人",
            "社会性死亡", "羞耻", "怯懦", "cowardice",
        }
        death_idx = None
        for e in events:
            # 直接检查是否包含排除关键词
            has_exclude = any(kw in e.event_type for kw in DEATH_EXCLUDE_KW)
            if has_exclude:
                continue  # 跳过排除的事件
            # 检查是否包含本人死亡关键词
            has_death = any(kw in e.event_type for kw in ["死亡", "去世", "逝世", "身亡", "亡故", "故去", "辞世"])
            if has_death:
                death_idx = e.index
                break
        if death_idx is not None:
            for e in events:
                if e.index > death_idx and e.event_type not in ("身后事", "遗产", "死亡追忆"):
                    issues.append(Issue(
                        code="L1-002", severity=Severity.FATAL,
                        message=f"人物在{e.year}年死亡后仍发生事件",
                        event_index=e.index,
                        suggestion="移除死亡后的事件"
                    ))
        return issues

    def _check_causal_adequacy(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        for e in events:
            if not e.causes:
                effect_w = self._weight(e.event_type + e.description, self.EFFECT_WEIGHT)
                if effect_w >= 3:
                    nearby = [ev for ev in events if ev != e and abs(ev.year - e.year) <= 2]
                    has_cause = any(self._weight(ev.event_type, self.CAUSE_WEIGHT) > 0 for ev in nearby)
                    if not has_cause:
                        issues.append(Issue(
                            code="L2-002", severity=Severity.SERIOUS,
                            message=f"事件'{e.event_type}'是重大转折但缺乏前置触发",
                            event_index=e.index,
                            suggestion="增加该事件的前置原因事件"
                        ))
        return issues

    def _check_event_gaps(self, events: List[ValidatorEvent], birth_year: int) -> List[Issue]:
        issues = []
        if len(events) < 3:
            return issues
        sorted_events = sorted(events, key=lambda e: e.year)
        for i in range(1, len(sorted_events)):
            gap = sorted_events[i].year - sorted_events[i - 1].year
            avg_age = (sorted_events[i].age + sorted_events[i - 1].age) / 2
            threshold = 10 if avg_age >= 18 else 6
            if gap > threshold:
                issues.append(Issue(
                    code="T1-004", severity=Severity.MINOR,
                    message=f"{sorted_events[i-1].year}年到{sorted_events[i].year}年间隔{gap}年，空白较大",
                    event_index=sorted_events[i].index,
                    suggestion="增加此期间的重要事件"
                ))
        return issues

    def _weight(self, text: str, weight_map: Dict[str, int]) -> int:
        return max((w for k, w in weight_map.items() if k in text), default=0)


class TemporalValidator:
    """时间现实性检测"""

    AGE_LIMITS = [
        ("入学", 5, 10), ("结婚", 16, 80), ("生子", 14, 55),
        ("当兵", 16, 35), ("退休", 50, 80), ("创业", 16, 75),
    ]
    MIN_INTERVALS = [
        ("结婚", "生子", 270), ("入学", "毕业", 365), ("入职", "晋升", 180),
        ("怀孕", "生子", 240), ("重伤", "康复", 180), ("出生", "走路", 300),
    ]

    def check(self, events: List[ValidatorEvent], birth_year: int) -> List[Issue]:
        issues = []
        issues.extend(self._check_age(events))
        issues.extend(self._check_intervals(events))
        issues.extend(self._check_mutually_exclusive(events))
        return issues

    def _check_age(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        for e in events:
            for kw, min_age, max_age in self.AGE_LIMITS:
                if kw in e.event_type:
                    if e.age < min_age:
                        issues.append(Issue(
                            code="T1-001", severity=Severity.SERIOUS,
                            message=f"{kw}发生在{e.age}岁，低于最低年龄{min_age}岁",
                            event_index=e.index,
                            suggestion=f"将{kw}移至{min_age}岁之后"
                        ))
                    elif e.age > max_age:
                        issues.append(Issue(
                            code="T1-001", severity=Severity.SERIOUS,
                            message=f"{kw}发生在{e.age}岁，高于最高年龄{max_age}岁",
                            event_index=e.index,
                            suggestion=f"将{kw}移至{max_age}岁之前"
                        ))
        return issues

    def _check_intervals(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        sorted_events = sorted(events, key=lambda e: (e.year, e.index))
        for i in range(1, len(sorted_events)):
            prev, curr = sorted_events[i - 1], sorted_events[i]
            interval_days = (date(curr.year, 1, 1) - date(prev.year, 1, 1)).days
            for kw1, kw2, min_days in self.MIN_INTERVALS:
                if kw1 in prev.event_type and kw2 in curr.event_type:
                    if 0 < interval_days < min_days:
                        issues.append(Issue(
                            code="T1-002", severity=Severity.SERIOUS,
                            message=f"{prev.event_type}到{curr.event_type}间隔{interval_days // 30}个月，不足以完成变化",
                            event_index=curr.index,
                            suggestion=f"增加间隔至至少{min_days // 30}个月"
                        ))
        return issues

    def _check_mutually_exclusive(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        from collections import defaultdict
        by_year = defaultdict(list)
        for e in events:
            by_year[e.year].append(e)
        for year, year_events in by_year.items():
            types = [e.event_type for e in year_events]
            if "入学" in types and "退休" in types:
                issues.append(Issue(
                    code="T1-006", severity=Severity.FATAL,
                    message=f"{year}年同时出现入学和退休，互斥",
                    event_index=year_events[types.index("退休")].index
                ))
            if "结婚" in types and "出家" in types:
                issues.append(Issue(
                    code="T1-006", severity=Severity.FATAL,
                    message=f"{year}年同时出现结婚和出家，互斥",
                    event_index=year_events[types.index("出家")].index
                ))
        return issues


class PsychologicalValidator:
    """心理常识性检测"""

    TRAUMA_KW = ["死亡", "丧", "重伤", "重病", "性侵", "暴力", "战争", "灾", "破产", "入狱"]

    def check(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        issues.extend(self._check_trait_continuity(events))
        issues.extend(self._check_trauma_persistence(events))
        return issues

    def _check_trait_continuity(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        attrs = {}
        for e in events:
            for attr, change in e.attribute_changes.items():
                # outcomes 格式为 [min, max] 或单个数值
                if isinstance(change, list):
                    change = sum(change) / len(change)  # 取平均值
                prev = attrs.get(attr, 0)
                new = prev + change
                if abs(change) > 40:
                    is_extreme = any(kw in e.event_type for kw in ["死亡", "重伤", "战争", "破产"])
                    if not is_extreme:
                        issues.append(Issue(
                            code="P1-001", severity=Severity.SERIOUS,
                            message=f"属性{attr}变化剧烈({prev:.0f}→{new:.0f})，但事件强度不足",
                            event_index=e.index,
                            suggestion="减小变化幅度或增加过渡事件"
                        ))
                attrs[attr] = new
        return issues

    def _check_trauma_persistence(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        trauma_events = [e for e in events if any(kw in e.event_type for kw in self.TRAUMA_KW)]
        for trauma in trauma_events:
            later = [e for e in events if trauma.year < e.year <= trauma.year + 3]
            has_effect = any(
                any(kw in e.description for kw in ["阴影", "梦", "怕", "失眠", "抑郁", "焦虑", "想起"])
                for e in later
            )
            is_severe = any(kw in trauma.event_type for kw in ["死亡", "重伤", "性侵", "战争", "灾"])
            if is_severe and not has_effect and later:
                issues.append(Issue(
                    code="P2-003", severity=Severity.SERIOUS,
                    message=f"严重创伤'{trauma.event_type}'后无持续影响描写",
                    event_index=trauma.index,
                    suggestion="增加创伤后1-3年的持续心理影响描写"
                ))
        return issues


class NarrativeValidator:
    """叙事逻辑性检测"""

    MAJOR_KW = ["彻底改变", "从此", "离婚", "分手", "自杀", "离家出走", "信仰崩塌"]
    FORESHADOW_KW = ["不满", "犹豫", "困惑", "压力", "矛盾", "问题", "困难", "越来越"]
    COINCIDENCE_KW = ["正好", "刚好", "碰巧", "偶然", "没想到", "居然"]

    def check(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        issues.extend(self._check_foreshadow(events))
        issues.extend(self._check_coincidence(events))
        issues.extend(self._check_life_stage_coverage(events))
        return issues

    def _check_foreshadow(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        for i, e in enumerate(events):
            is_major = any(kw in e.event_type or kw in e.description for kw in self.MAJOR_KW)
            if not is_major or i < 1:
                continue
            prev_events = events[max(0, i - 3):i]
            has_foreshadow = any(
                any(kw in pe.description for kw in self.FORESHADOW_KW)
                for pe in prev_events
            )
            if not has_foreshadow:
                issues.append(Issue(
                    code="N1-001", severity=Severity.SERIOUS,
                    message=f"事件'{e.event_type}'是重大转折但缺乏铺垫",
                    event_index=e.index,
                    suggestion="在转折前增加1-2个暗示性事件"
                ))
        return issues

    def _check_coincidence(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        coincidences = sum(1 for e in events if any(kw in e.description for kw in self.COINCIDENCE_KW))
        total = len(events)
        if total > 0 and coincidences / total > 0.3:
            issues.append(Issue(
                code="N1-003", severity=Severity.SERIOUS,
                message=f"故事中{coincidences}/{total}个事件依赖巧合，比例偏高",
                suggestion="将部分巧合改为主动行为或关系网络推动"
            ))
        return issues

    def _check_life_stage_coverage(self, events: List[ValidatorEvent]) -> List[Issue]:
        issues = []
        stages = [(0, 5), (6, 12), (13, 18), (19, 25), (26, 40), (41, 55), (56, 70)]
        stage_names = ["幼年", "童年", "青春期", "青年初期", "壮年", "中年", "中老年"]
        ages = [e.age for e in events if e.age > 0]
        if not ages:
            return issues
        max_age = max(ages)
        for (min_a, max_a), name in zip(stages, stage_names):
            if max_age <= max_a:
                break
            has_events = any(min_a <= e.age <= max_a for e in events)
            if not has_events and max_age > max_a:
                issues.append(Issue(
                    code="D1-003", severity=Severity.MINOR,
                    message=f"人生阶段'{name}'({min_a}-{max_a}岁)无任何事件",
                    suggestion=f"在{name}阶段增加至少1个关键事件"
                ))
        return issues


class StoryValidator:
    """
    故事逻辑验证器
    整合所有检测维度，对人生故事进行逻辑性和一致性检测
    """

    MAX_RETRIES = 5           # 最大重试次数
    SERIOUS_THRESHOLD = 3     # 超过此数量SERIOUS问题则建议重试

    def __init__(self):
        self.validators = [
            LogicValidator(),
            TemporalValidator(),
            PsychologicalValidator(),
            NarrativeValidator(),
        ]

    def validate(self, timeline: List[Dict[str, Any]], character: Dict[str, Any]) -> ValidationResult:
        """
        对时间线进行逻辑检测，返回检测结果
        """
        vchar, vevents = timeline_to_validator_format(timeline, character)
        all_issues: List[Issue] = []

        # 需要 birth_year 的验证器
        needs_birth_year = (LogicValidator, TemporalValidator)
        for validator in self.validators:
            if isinstance(validator, needs_birth_year):
                issues = validator.check(vevents, vchar.birth_year)
            else:
                issues = validator.check(vevents)
            all_issues.extend(issues)

        return ValidationResult.from_issues(all_issues)

    def validate_with_retry(
        self,
        generate_fn,
        character: Dict[str, Any],
        selected_structure_ids: List[str],
        initial_seed: Optional[int] = None
    ) -> Tuple[List[Dict[str, Any]], ValidationResult]:
        """
        带重试的故事生成

        Args:
            generate_fn: 生成函数，签名为 (character, structure_ids, seed) -> timeline
            character: 人物数据
            selected_structure_ids: 选中的社会结构
            initial_seed: 初始随机种子

        Returns:
            (timeline, validation_result) 元组
        """
        seed = initial_seed if initial_seed is not None else random.randint(0, 999999)
        best_timeline: Optional[List[Dict[str, Any]]] = None
        best_result: Optional[ValidationResult] = None

        for retry in range(self.MAX_RETRIES):
            current_seed = seed + retry
            timeline = generate_fn(character, selected_structure_ids, current_seed)
            result = self.validate(timeline, character)

            if result.passed and result.serious_count <= self.SERIOUS_THRESHOLD:
                result.retry_count = retry
                return timeline, result

            # 记录最佳结果（FATAL最少的那次）
            if best_result is None or result.fatal_count < best_result.fatal_count:
                best_timeline = timeline
                best_result = result

        # 达到最大重试次数，返回最佳结果
        if best_result is not None:
            best_result.retry_count = self.MAX_RETRIES
            return best_timeline, best_result

        # 万一下面逻辑出问题，返回最后一次
        result.retry_count = self.MAX_RETRIES
        return timeline, result


# =====================================================================
# 便捷函数
# =====================================================================

_validator: Optional[StoryValidator] = None

def get_validator() -> StoryValidator:
    global _validator
    if _validator is None:
        _validator = StoryValidator()
    return _validator


def validate_story(timeline: List[Dict[str, Any]], character: Dict[str, Any]) -> ValidationResult:
    """快速验证接口"""
    return get_validator().validate(timeline, character)
