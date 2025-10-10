from .compound_parser import parse_formula
from ..utils.find_element import find_element


def relative_molecular_mass(text: str) -> float:
    """计算相对分子质量"""
    normalized, charge = parse_formula(text)
    molar_mass = 0
    for el, cnt in normalized.items():
        molar_mass += cnt * find_element(el)["atomic_mass"]
    return molar_mass
