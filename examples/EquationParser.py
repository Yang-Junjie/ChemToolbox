from ChemToolbox.core.equation_parser import parse_equation

equations = [
    "Ba^{2+} + SO_4^{2-} -> BaSO_4",
    "MnO_4^{-} + Fe^{2+} + H^{+} -> Mn^{2+} + Fe^{3+} + H_2O",
]

for eq in equations:
    result = parse_equation(eq)
    left = result["left"]
    right = result["right"]

    print("反应物:", left["parts"])
    print("生成物:", right["parts"])
    print("反应物包含的元素:", left["total"])
    print("生成物包含的元素:", right["total"])
    print("反应物电荷:", left["charges"])
    print("生成物电荷:", right["charges"])
    print("涉及的全部元素:", result["elements"])
    print()
