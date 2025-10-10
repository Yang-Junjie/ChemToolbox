import re
from collections import defaultdict, namedtuple
import json

Token = namedtuple("Token", ["type", "value"])

_token_spec = [
    ("SPACE", r"\s+"),  # 空白
    ("ELEMENT", r"[A-Z][a-z]?"),  # 元素符号
    ("NUMBER", r"\d+"),  # 数字
    ("CARET", r"\^"),  # 上标符号
    ("UNDERS", r"_"),  # 下标符号
    ("LBRACE", r"\{"),  # 左花括号
    ("RBRACE", r"\}"),  # 右花括号
    ("LPAREN", r"\("),  # 左括号
    ("RPAREN", r"\)"),  # 右括号
    ("PLUS", r"\+"),  # 加号
    ("MINUS", r"-"),  # 减号
    ("EOF", r"$"),  # 结尾
]
_token_regex = re.compile("|".join("(?P<%s>%s)" % pair for pair in _token_spec))


def lex(text):
    pos, tokens = 0, []
    # 如果pos未到达文本末尾，则继续解析
    while pos < len(text):
        # 解析一个token
        m = _token_regex.match(text, pos)
        if not m:
            raise SyntaxError(f"非法字符: {text[pos:]}")
        # 合法字符则，生成一个token
        typ, val = m.lastgroup, m.group(m.lastgroup)
        pos = m.end()
        if typ == "SPACE":
            continue
        tokens.append(Token(typ, val))
    tokens.append(Token("EOF", ""))
    return tokens


def parse_charge(s):
    """解析电荷字符串，返回整数电荷"""
    s = s.strip()
    if s == "+":
        return 1
    if s == "-":
        return -1
    m = re.match(r"(\d+)([+-])", s)
    if not m:
        raise SyntaxError(f"非法电荷格式 ^{{{s}}}")
    n = int(m.group(1))
    sign = 1 if m.group(2) == "+" else -1
    return n * sign


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def cur(self):
        """获取当前token"""
        return self.tokens[self.i]

    def eat(self, *types):
        """如果当前token类型在types中，则消耗掉并返回，否则报错"""
        if self.cur().type in types:
            t = self.cur()
            self.i += 1
            return t
        raise SyntaxError(f"期望 {types}，得到 {self.cur()}")

    def parse(self):
        comp, charge = self.parse_formula()
        if self.cur().type != "EOF":
            raise SyntaxError(f"解析未结束：{self.cur()}")
        return comp, charge

    def parse_unit(self):
        """解析一个元素组成"""
        charge = 0
        # 元素
        if self.cur().type == "ELEMENT":
            el = self.eat("ELEMENT").value
            count = 1
            if self.cur().type == "UNDERS":
                count = self.parse_number()
            comp = defaultdict(int)
            comp[el] += count
            # 可能有电荷
            if self.cur().type == "CARET":
                s = self.read_braced_content()
                charge += parse_charge(s)
            return comp, charge

        # 递归括号
        if self.cur().type == "LPAREN":
            self.eat("LPAREN")
            inner = defaultdict(int)
            charge = 0
            while self.cur().type not in ("RPAREN", "EOF"):
                comp, ch = self.parse_unit()
                for k, v in comp.items():
                    inner[k] += v
                charge += ch
            self.eat("RPAREN")
            mult = 1
            if self.cur().type == "UNDERS":
                mult = self.parse_number()
            if self.cur().type == "CARET":
                s = self.read_braced_content()
                charge += parse_charge(s)
            comp = defaultdict(int)
            for k, v in inner.items():
                comp[k] += v * mult
            return comp, charge

        raise SyntaxError(f"意外的符号: {self.cur()}")

    def parse_number(self):
        """解析下标数字"""
        self.eat("UNDERS")
        if self.cur().type == "LBRACE":
            self.eat("LBRACE")
            n = int(self.eat("NUMBER").value)
            self.eat("RBRACE")
        else:
            n = int(self.eat("NUMBER").value)
        return n

    def read_braced_content(self):
        """读取花括号内的内容，当前token是CARET"""
        self.eat("CARET")
        if self.cur().type != "LBRACE":
            raise SyntaxError("上标必须使用花括号，如 ^{2+}")
        self.eat("LBRACE")
        content = ""
        while self.cur().type not in ("RBRACE", "EOF"):
            content += self.cur().value
            self.i += 1
        self.eat("RBRACE")
        return content.strip()

    def parse_formula(self):
        """解析化学式，返回元素组成和总电荷"""
        total = defaultdict(int)
        total_charge = 0
        while self.cur().type in ("ELEMENT", "LPAREN"):
            comp, charge = self.parse_unit()
            for k, v in comp.items():
                total[k] += v
            total_charge += charge
        # 如果有整体电荷上标
        if self.cur().type == "CARET":
            s = self.read_braced_content()
            total_charge += parse_charge(s)
        return dict(total), total_charge


def parse_formula(text):
    """解析化学式，返回元素组成和总电荷"""
    tokens = lex(text)
    p = Parser(tokens)
    comp, charge = p.parse()
    return comp, charge


def parse_formula_json(text):
    """解析化学式，返回JSON格式"""
    comp, charge = parse_formula(text)
    data = {"composition": comp, "charge": charge}  
    return json.dumps(data, ensure_ascii=False)



