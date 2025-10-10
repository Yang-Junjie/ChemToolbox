import numpy as np
from sympy import Matrix
from .equation_parser import parse_equation


class EquationBalancer:
    """
    化学方程式配平器
    使用线性代数方法配平化学反应方程式，支持离子电荷的处理。
    """

    def __init__(self):
        self.equation = None
        self.parsed = None
        self.left = None
        self.right = None
        self.elements = None
        self.all_parts = None

    def set_equation(self, equation: str):
        """设置需要配平的化学方程式"""
        self.equation = equation
        self.parsed = parse_equation(equation)
        self.left = self.parsed["left"]
        self.right = self.parsed["right"]
        self.elements = self.parsed["elements"]
        self.all_parts = self.left["parts"] + self.right["parts"]

    def create_matrix(self) -> np.ndarray:
        """创建用于求解的系数矩阵"""
        if self.parsed is None:
            raise ValueError("请先使用 set_equation() 设置方程式")

        # 初始化矩阵, 行数为元素种类数+1（电荷守恒），列数为化合物总数
        n_elements = len(self.elements)
        n_compounds = len(self.all_parts)

        # 创建矩阵
        A = np.zeros((n_elements + 1, n_compounds), dtype=int)

        # 填充矩阵
        for j, formula in enumerate(self.left["formulas"]):
            for i, elem in enumerate(self.elements):
                A[i, j] = -formula.get(elem, 0)

            A[-1, j] = -self.left["charges"][j]

        offset = len(self.left["formulas"])
        for j, formula in enumerate(self.right["formulas"], start=offset):
            for i, elem in enumerate(self.elements):
                A[i, j] = formula.get(elem, 0)

            A[-1, j] = self.right["charges"][j - offset]

        return A

    def balance(self) -> list[int]:
        """配平方程式，返回各化合物的系数列表"""
        A = self.create_matrix()
        M = Matrix(A)
        # 求解矩阵的零空间
        null_space = M.nullspace()

        if not null_space:
            raise ValueError(
                "方程式无法配平，未找到解，请检查输入的化学方程式是否正确。"
            )
        # 取第一个基向量作为解
        vec = null_space[0]
        # 将解向量转换为整数系数
        lcm_denom = np.lcm.reduce([r.q for r in vec])
        coeffs = [int(r * lcm_denom) for r in vec]

        # 确保所有系数为正
        if all(c <= 0 for c in coeffs):
            coeffs = [-c for c in coeffs]

        return coeffs

    def get_balanced_equation(self) -> str:
        """返回配平后的化学方程式字符串"""
        if self.parsed is None:
            raise ValueError("请先使用 set_equation() 设置方程式")

        coeffs = self.balance()
        parts = self.all_parts
        n_left = len(self.left["parts"])

        left_str = " + ".join(
            f"{coeffs[i]} {parts[i]}" if coeffs[i] != 1 else parts[i]
            for i in range(n_left)
        )

        right_str = " + ".join(
            (
                f"{coeffs[i + n_left]} {parts[i + n_left]}"
                if coeffs[i + n_left] != 1
                else parts[i + n_left]
            )
            for i in range(len(parts) - n_left)
        )

        return f"{left_str} -> {right_str}"
