import re
def parse_equation(equation: str) -> tuple[list, list]:
    """解析化学反应方程式，分离反应物和生成物"""
    # 分割反应物和生成物
    if "->" in equation:
        left_str, right_str = equation.split("->")
    else:
        raise ValueError("化学反应方程式必须包含 -> 符号")
    left_part = []
    right_part = []

 
    # 使用+分割
    # 这种情况下，需要确保不会在离子的+电荷处分割
    # 先按+分割，然后尝试修复可能被错误分割的离子
    raw_parts = re.split(r"(\+)", left_str)
    i = 0
    while i < len(raw_parts):
        part = raw_parts[i].strip()
        # 检查是否是元素
        if part and part not in ("+"):
            # 检查是否需要与下一部分合并（可能是离子电荷）：如果是正电荷离子可能会被分割成类似"Ba^{2", "+", "}"这种形式
            if i + 1 < len(raw_parts) and "{" in part and "}" not in part:
                # 可能是离子电荷被分割了，尝试合并
                combined = part + raw_parts[i + 1]
                if i + 2 < len(raw_parts) and "}" not in combined:
                    combined += raw_parts[i + 2]
                left_part.append(combined.strip())
                i += 3  # 跳过已合并的部分
            else:
                left_part.append(part)
                i += 1
        else:
            i += 1

    # 处理生成物部分，方法同上
    raw_parts = re.split(r"(\+)", right_str)
    i = 0
    while i < len(raw_parts):
        part = raw_parts[i].strip()
        if part and part not in ("+"):
            if i + 1 < len(raw_parts) and "{" in part and "}" not in part:
                combined = part + raw_parts[i + 1]
                if i + 2 < len(raw_parts) and "}" not in combined:
                    combined += raw_parts[i + 2]
                right_part.append(combined.strip())
                i += 3
            else:
                right_part.append(part)
                i += 1
        else:
            i += 1

    return left_part, right_part
