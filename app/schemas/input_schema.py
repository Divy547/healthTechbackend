from pydantic import BaseModel
from typing import List, Dict, Any

class DrugRequest(BaseModel):
    patient_data: Dict[str, Any]
    drugs: List[str]
