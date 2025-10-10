from fastapi import APIRouter, Response, status, HTTPException
from ChemToolbox.core.equation_parser import parse_equation, get_all_elements
from ChemToolbox.core.equaion_balancer import EquationBalancer
from fastapi.responses import JSONResponse
import json

router = APIRouter(prefix="/equations", tags=["Chemical Equations"])

# 实例化配平器
balancer = EquationBalancer()


@router.get("/balance/{equation}")
def balance_equation(equation: str):
    """
    化学方程式配平接口
    请求参数:
      - equation: 字符串，化学方程式
    返回:
      - 配平后的方程式字符串，如果无法配平则返回错误信息
    """
    try:
        balancer.set_equation(equation)
        balanced_coefficients = balancer.balance()
        balanced = balancer.get_balanced_equation()
        result = {
            "input": equation,
            "balanced_cofficients": balanced_coefficients,
            "balanced_equation": balanced,
        }
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
