from fastapi import APIRouter
from app.schemas.input_schema import DrugRequest

router = APIRouter()

@router.post("/analyze")
def analyze_patient(data: DrugRequest):
    return {"status": "processing pipeline not connected yet"}
