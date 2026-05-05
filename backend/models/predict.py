from pydantic import BaseModel
from typing import List, Literal


class PredictionRequest(BaseModel):
    smiles: str


class TargetResult(BaseModel):
    chembl_id: str
    uniprot_id: str
    target_name: str
    chance: float


class PredictionResponse(BaseModel):
    id: str
    table: List[TargetResult] = []


class ReportRequest(BaseModel):
    id: str
    extension: Literal['txt', 'pdf', 'csv']
