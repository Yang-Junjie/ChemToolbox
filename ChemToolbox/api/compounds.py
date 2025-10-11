from fastapi import APIRouter, HTTPException, Response
from ChemToolbox.core.relative_molecular_mass import relative_molecular_mass
from fastapi.responses import JSONResponse
import json

router = APIRouter(prefix="/compounds", tags=["Chemical Compounds"])


@router.get("/molar_mass/{formula}")
def get_molar_mass(formula: str):
    try:
        mass = relative_molecular_mass(formula)
        return {"formula": formula, "molar_mass": mass}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))