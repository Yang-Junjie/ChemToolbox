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
