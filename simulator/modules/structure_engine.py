"""
社会结构交互引擎
计算社会结构对人物属性的影响，以及结构间的交互作用
"""
import yaml
import os
from typing import Dict, List, Any, Optional


class StructureEngine:
    """社会结构交互计算引擎"""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir
        self.structures = self._load_structures()

    def _load_structures(self) -> List[Dict[str, Any]]:
        """加载社会结构定义"""
        structures_path = os.path.join(self.data_dir, "structures.yaml")
        with open(structures_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data["structures"]

    def get_structure(self, struct_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取社会结构"""
        for s in self.structures:
            if s["id"] == struct_id:
                return s
        return None

    def get_all_structures(self) -> List[Dict[str, Any]]:
        """获取所有社会结构"""
        return self.structures

    def get_structures_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """按理论家分类组织的社会结构"""
        categories = {}
        for s in self.structures:
            theorist = s.get("theorist", "其他")
            if theorist not in categories:
                categories[theorist] = []
            categories[theorist].append(s)
        return categories

    def calculate_structure_effects(
        self,
        selected_structure_ids: List[str],
        current_state: Dict[str, float]
    ) -> Dict[str, float]:
        """
        计算选中社会结构对人物当前状态的综合影响

        Args:
            selected_structure_ids: 选中的社会结构ID列表
            current_state: 人物当前状态（属性向量）

        Returns:
            状态变化字典 {属性名: 变化量}
        """
        total_effects = {}

        for struct_id in selected_structure_ids:
            struct = self.get_structure(struct_id)
            if not struct:
                continue

            # 获取该结构的所有效果
            effects = struct.get("effects", {})

            # 计算直接效果
            for attr, change in effects.items():
                if isinstance(change, (int, float)):
                    if attr not in total_effects:
                        total_effects[attr] = 0.0
                    total_effects[attr] += change

            # 计算交互效果
            interactions = struct.get("interactions", [])
            for interaction in interactions:
                target = interaction.get("target")
                effect = interaction.get("effect", 0)
                target_struct = self.get_structure(target)

                # 如果目标结构也在选中列表中，应用交互效果
                if target in selected_structure_ids and target_struct:
                    # 交互效果影响当前状态中的相关属性
                    if target not in total_effects:
                        total_effects[target] = 0.0
                    total_effects[target] += effect

        # 归一化效果，防止过大
        for k, v in total_effects.items():
            total_effects[k] = max(-1.0, min(1.0, v))

        return total_effects

    def calculate_action_weights(
        self,
        selected_structure_ids: List[str],
        action_definitions: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        根据选中的社会结构计算各类社会行动的权重

        Args:
            selected_structure_ids: 选中的社会结构ID列表
            action_definitions: 行动类型定义列表

        Returns:
            行动权重字典 {行动ID: 权重}
        """
        weights = {}

        for action in action_definitions:
            action_id = action["id"]
            weight_factors = action.get("weight_factors", {})

            base_weight = 0.2  # 基础权重
            total_weight = base_weight

            for factor, coefficient in weight_factors.items():
                # 检查是否有结构提供这个因素
                for struct_id in selected_structure_ids:
                    struct = self.get_structure(struct_id)
                    if struct:
                        effects = struct.get("effects", {})
                        if factor in effects:
                            total_weight += effects[factor] * coefficient

            weights[action_id] = max(0.0, min(1.0, total_weight))

        # 归一化权重
        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}

        return weights

    def get_structure_interactions_summary(
        self,
        selected_structure_ids: List[str]
    ) -> List[str]:
        """
        生成选中社会结构之间交互的文本摘要

        Args:
            selected_structure_ids: 选中的社会结构ID列表

        Returns:
            交互效果描述列表
        """
        summaries = []

        for struct_id in selected_structure_ids:
            struct = self.get_structure(struct_id)
            if not struct:
                continue

            interactions = struct.get("interactions", [])
            for interaction in interactions:
                target = interaction.get("target")
                effect = interaction.get("effect", 0)

                if target in selected_structure_ids:
                    target_struct = self.get_structure(target)
                    if target_struct:
                        effect_desc = "增强" if effect > 0 else "削弱"
                        summaries.append(
                            f"*{struct['name']}* {effect_desc} *{target_struct['name']}*"
                        )

        return summaries

    def apply_effects_to_state(
        self,
        current_state: Dict[str, float],
        effects: Dict[str, float]
    ) -> Dict[str, float]:
        """
        将效果应用到当前状态，生成新状态

        Args:
            current_state: 当前状态
            effects: 效果变化量

        Returns:
            新状态
        """
        new_state = current_state.copy()

        for attr, change in effects.items():
            if attr not in new_state:
                new_state[attr] = 0.0
            new_state[attr] = max(-1.0, min(1.0, new_state[attr] + change))

        return new_state

    def get_structural_summary(
        self,
        selected_structure_ids: List[str]
    ) -> str:
        """
        生成社会结构的综合描述文本

        Args:
            selected_structure_ids: 选中的社会结构ID列表

        Returns:
            描述文本
        """
        lines = []
        lines.append("## 选定的社会结构\n")

        theorists_structures = {}
        for struct_id in selected_structure_ids:
            struct = self.get_structure(struct_id)
            if struct:
                theorist = struct.get("theorist", "其他")
                if theorist not in theorists_structures:
                    theorists_structures[theorist] = []
                theorists_structures[theorist].append(struct)

        for theorist, structures in theorists_structures.items():
            lines.append(f"### {theorist}\n")
            for s in structures:
                lines.append(f"- **{s['emoji']} {s['name']}**: {s['description']}")
            lines.append("")

        # 添加交互效果
        interactions = self.get_structure_interactions_summary(selected_structure_ids)
        if interactions:
            lines.append("### 结构交互\n")
            for i in interactions:
                lines.append(f"- {i}")

        return "\n".join(lines)


if __name__ == "__main__":
    # 测试代码
    engine = StructureEngine()
    print("可用的社会结构：")
    for s in engine.get_all_structures():
        print(f"  {s['emoji']} {s['name']} ({s['theorist']})")