# ChemToolbox

## 项目简介

ChemToolbox是一个功能丰富的Python化学工具箱，提供多种化学计算和分析功能，支持双重使用模式：既可作为独立Python库直接导入使用，也可作为Web后端服务通过API调用。

## 功能特性

- **元素查询**：查找元素的基本信息（原子序数、原子量、元素类型等）
- **相对分子质量计算**：计算化合物的相对分子质量
- **化学式解析**：解析复杂的化学式，支持括号和电荷表示
- **化学方程式解析**：分析化学反应方程式的反应物、生成物和元素组成
- **化学方程式配平**：自动配平化学方程式，支持离子方程式

## 安装方法

使用pip安装ChemToolbox：

```bash
pip install -e .
```

### 依赖项

项目主要依赖以下Python库：

- numpy>=1.20.0
- sympy (用于方程式配平)
- fastapi (用于Web服务)
- uvicorn (FastAPI的ASGI服务器)

安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方式

### 1. 作为独立Python库使用

#### 元素查询

```python
from ChemToolbox.utils.find_element import find_element

# 查询元素信息
element = find_element("Cu")
print(f"元素名称: {element['name_cn']}")
print(f"原子量: {element['atomic_mass']}")
```

#### 相对分子质量计算

```python
from ChemToolbox.core.relative_molecular_mass import relative_molecular_mass

# 计算水分子的摩尔质量
water_mass = relative_molecular_mass("H_2O")
print(f"水的摩尔质量: {water_mass:.4f}")

# 计算离子的摩尔质量
 sulfate_mass = relative_molecular_mass("SO_4^{2-}")
print(f"硫酸根离子的摩尔质量: {sulfate_mass:.4f}")
```

#### 化学式解析

```python
from ChemToolbox.core.compound_parser import parse_formula

# 解析化学式，返回元素组成和电荷
composition, charge = parse_formula("Ca(CN)_2")
print(f"元素组成: {composition}")
print(f"电荷: {charge}")
```

#### 化学方程式配平

```python
from ChemToolbox.core.equaion_balancer import EquationBalancer

# 创建配平器实例
balancer = EquationBalancer()

# 设置要配平的方程式
balancer.set_equation("Ba^{2+} + SO_4^{2-} -> BaSO_4")

# 获取配平后的方程式
balanced_equation = balancer.get_balanced_equation()
print(f"配平后的方程式: {balanced_equation}")

# 获取配平系数
coefficients = balancer.balance()
print(f"配平系数: {coefficients}")
```

#### 化学方程式解析

```python
from ChemToolbox.core.equation_parser import parse_equation

# 解析方程式
result = parse_equation("Ba^{2+} + SO_4^{2-} -> BaSO_4")

# 获取反应物和生成物信息
print(f"反应物: {result['left']['parts']}")
print(f"生成物: {result['right']['parts']}")
print(f"反应物包含的元素: {result['left']['total']}")
print(f"生成物包含的元素: {result['right']['total']}")
print(f"涉及的全部元素: {result['elements']}")
```

### 2. 作为Web后端API使用

#### 启动API服务

```bash
cd ChemToolbox
uvicorn main:app --reload
```

服务启动后，可通过 http://localhost:8000 访问API

#### API端点

##### 化合物相关API

- **计算摩尔质量**
  - URL: `/api/compounds/molar_mass/{formula}`
  - 方法: GET
  - 参数: formula - 化合物的化学式
  - 返回: JSON格式的摩尔质量数据

##### 元素相关API

- **查询元素信息**
  - URL: `/api/elements/{symbol}`
  - 方法: GET
  - 参数: symbol - 元素符号
  - 返回: JSON格式的元素信息

##### 方程式相关API

- **配平方程式**
  - URL: `/api/equations/balance/{equation}`
  - 方法: GET
  - 参数: equation - 化学方程式
  - 返回: JSON格式的配平结果

## 项目结构

```
ChemToolbox/
├── ChemToolbox/             # 主源码目录
│   ├── api/                 # API接口实现
│   │   ├── compounds.py     # 化合物相关API
│   │   ├── equations.py     # 方程式相关API
│   │   └── utils.py         # 工具相关API
│   ├── core/                # 核心功能模块
│   │   ├── compound_parser.py      # 化学式解析器
│   │   ├── equaion_balancer.py     # 方程式配平器
│   │   ├── equation_parser.py      # 方程式解析器
│   │   └── relative_molecular_mass.py  # 相对分子质量计算
│   ├── data/                # 数据文件
│   │   └── elements.json    # 元素数据
│   ├── utils/               # 工具函数
│   │   └── find_element.py  # 元素查找功能
│   ├── __init__.py
│   └── main.py              # Web服务入口
├── examples/                # 示例代码
│   ├── CompoundParser.py    # 化学式解析示例
│   ├── ComputeMolarMass.py  # 摩尔质量计算示例
│   ├── EquationBalancer.py  # 方程式配平示例
│   ├── EquationParser.py    # 方程式解析示例
│   └── FindElement.py       # 元素查找示例
├── requirements.txt         # 项目依赖
├── setup.py                 # 安装配置
└── README.md                # 项目说明文档
```

## 开发计划

- 添加热力学计算功能（焓、熵、自由能）
- 增强化学式解析器，支持更复杂的化学式表示


## 许可证

本项目采用MIT许可证。