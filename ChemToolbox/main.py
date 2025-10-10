from fastapi import FastAPI
from api.equations import router as equations_router
from api.utils import router as utils_router
from api.compounds import router as compounds_router

app = FastAPI(title="ChemToolbox API")

# 注册各个模块的路由
app.include_router(equations_router, prefix="/api")
app.include_router(utils_router, prefix="/api")
app.include_router(compounds_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to ChemToolbox API"}
