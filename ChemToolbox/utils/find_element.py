import json
from pathlib import Path
from functools import lru_cache


@lru_cache()
def _load_elements() -> list[dict]:
    """加载元素 JSON 并缓存"""
    elements_path = Path(__file__).parent.parent / "data" / "elements.json"
    with open(elements_path, encoding="utf-8-sig") as f:
        return json.load(f)


def find_element(symbol: str) -> dict | None:
    """查找元素，参数是元素符号（严格区分大小写），如果存在则返回完整 JSON 信息，否则返回 None"""
    data = _load_elements()
    for element in data:
        if element["symbol"] == symbol:
            return element
    return None


def get_table_elements():
    pass

def get_period(element: str) -> int | None:
    """获取元素的周期数"""
    el = find_element(element)
    if el:
        return el.get("period")
    return None

def get_group(element: str) -> int | None:
    """获取元素的组数"""
    el = find_element(element)
    if el:
        return el.get("group")
    return None

def get_atomic_number(element: str) -> int | None:
    """获取元素的原子序数"""
    el = find_element(element)
    if el:
        return el.get("atomic_number")
    return None

def get_atomic_mass(element: str) -> float | None:
    """获取元素的相对原子质量"""
    el = find_element(element)
    if el:
        return el.get("atomic_mass")
    return None

