import re
from .compound_parser import parse_formula
from collections import Counter


def parse_equation(equation: str):
    """解析化学反应方程式，分离反应物和生成物，并提取元素、电荷信息"""

    # 分割反应物和生成物
    if "->" in equation:
        left_str, right_str = equation.split("->")
    else:
        raise ValueError("化学反应方程式必须包含 -> 符号")

    def split_parts(expr: str):
        """使用 + 分割化学式，同时避免将离子的电荷部分错误分割"""
        # 按 + 分割，注意电荷中的 + 可能会导致误分割
        raw_parts = re.split(r"(\+)", expr)
        parts = []
        i = 0
        while i < len(raw_parts):
            part = raw_parts[i].strip()
            # 检查是否是元素
            if part and part not in ("+"):
                # 检查是否需要与下一部分合并（可能是离子电荷）：
                # 如果是正电荷离子可能会被分割成类似 "Ba^{2", "+", "}" 这种形式
                if i + 1 < len(raw_parts) and "{" in part and "}" not in part:
                    # 可能是离子电荷被分割了，尝试合并
                    combined = part + raw_parts[i + 1]
                    if i + 2 < len(raw_parts) and "}" not in combined:
                        combined += raw_parts[i + 2]
                    parts.append(combined.strip())
                    i += 3  # 跳过已合并的部分
                else:
                    parts.append(part)
                    i += 1
            else:
                i += 1
        return parts

    def parse_side(parts):
        """解析方程一侧（反应物或生成物），提取元素、数量、电荷"""
        parsed = [
            parse_formula(p) for p in parts
        ]  # 每个 parse_formula 返回 (dict, charge)
        formulas = [f[0] for f in parsed]  # 提取化学式字典
        charges = [f[1] for f in parsed]  # 提取电荷
        # 将所有元素计数合并成一个总字典
        total = dict(sum((Counter(f) for f in formulas), Counter()))
        return {
            "parts": parts,
            "formulas": formulas,
            "charges": charges,
            "total": total,
        }

    # 分别解析反应物和生成物
    left = parse_side(split_parts(left_str))
    right = parse_side(split_parts(right_str))

    # 收集所有涉及的元素（用于构建配平方程的系数矩阵）
    elements = sorted(set(left["total"]) | set(right["total"]))

    # 返回结构化结果，方便后续配平方程
    return {"left": left, "right": right, "elements": elements}


def get_all_elements(equation: str) -> set:
    """获取化学反应方程式中所有涉及的元素"""
    left_part, left_formulas, _, right_part, right_formulas, _ = parse_equation(
        equation
    )
    elements = set()
    for formula in left_formulas + right_formulas:
        elements.update(formula.keys())
    return elements
