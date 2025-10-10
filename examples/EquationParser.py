import ChemToolbox.core.equation_parser 

equation = "Ba^{2+} + SO_4^{2-} -> BaSO_4"
left, right = ChemToolbox.core.equation_parser.parse_equation(equation)
print(f"方程式: {equation}")
print(f"反应物: {left}")
print(f"生成物: {right}")
print(f"涉及的元素: {ChemToolbox.core.equation_parser.get_all_elements(equation)}")
