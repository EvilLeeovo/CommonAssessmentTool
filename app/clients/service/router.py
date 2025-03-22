# predict_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..schema import PredictionInput  
from . import logic as ml_logic  

router = APIRouter(prefix="/predict", tags=["predict"])

class SwitchModelRequest(BaseModel):
    model_name: str

@router.get("/model")
async def get_current_model():
    return {"current_model": ml_logic.CURRENT_MODEL_NAME}

@router.post("/model")
async def switch_model(request: SwitchModelRequest):
    try:
        ml_logic.set_current_model(request.model_name)
        return {"message": f"change model to: {request.model_name}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
async def predict(input_data: PredictionInput):
    try:
        result = ml_logic.interpret_and_calculate(input_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
