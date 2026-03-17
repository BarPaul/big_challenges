from models.predict import PredictionRequest, PredictionResponse
from fastapi import APIRouter, HTTPException
from httpx import AsyncClient
from os import getenv


router = APIRouter(prefix="/predict")
AI_SERVICE_URL = getenv("AI_SERVICE_URL", "http://ai:8001")


@router.post("/biotargets", response_model=PredictionResponse)
async def predict_biotargets(request: PredictionRequest):
    async with AsyncClient() as client:
        try:
            response = await client.post(f"{AI_SERVICE_URL}/infer", json={"smiles": request.smiles})
            response.raise_for_status()
            return PredictionResponse(**response.json())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка AI сервиса: {str(e)}")
