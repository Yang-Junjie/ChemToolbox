from fastapi import APIRouter, Response, status
from ChemToolbox.utils.find_element import find_element

router = APIRouter(prefix="/elements", tags=["Elements"])


@router.get("/{symbol}")
def get_element(symbol: str):
    element = find_element(symbol)
    if element:
        return element
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="Element not found")
