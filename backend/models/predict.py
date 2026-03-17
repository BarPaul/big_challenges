from pydantic import BaseModel
from typing import List


class PredictionRequest(BaseModel):
    smiles: str


class TargetResult(BaseModel):
    target: str
    common_name: str
    uniprot_id: str
    chEMBL_id: str
    probability: float
    target_class: str


class PredictionResponse(BaseModel):
    table: List[TargetResult]
