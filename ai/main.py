import torch
import numpy as np
import pandas as pd
from rdkit import Chem
from chembl_webresource_client.new_client import new_client
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator
from transformers import AutoTokenizer, AutoModel
import joblib
import warnings

from uvicorn import run
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional

warnings.filterwarnings('ignore')

class DrugPredictionModel(torch.nn.Module):
    def __init__(self, input_dim=2816, num_targets=584, dropout_rate=0.45):
        super().__init__()
        self.mlp = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 512),
            torch.nn.ReLU(),
            torch.nn.Dropout(dropout_rate),
            torch.nn.Linear(512, 256),
            torch.nn.ReLU(),
            torch.nn.Dropout(dropout_rate),
            torch.nn.Linear(256, num_targets)
        )
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        return self.sigmoid(self.mlp(x))

model: Optional[DrugPredictionModel] = None
scaler = None
tokenizer = None
chembert_model = None
target_cols: List[str] = []
target_info_cache: Dict[str, Dict] = {}


def get_uniprot_from_chembl(chembl_id: str) -> Dict[str, str]:
    """
    Возвращает {"uniprot_id": "...", "target_name": "..."}.
    Если нет в кэше — делает запрос к ChEMBL и кэширует результат.
    """
    if chembl_id in target_info_cache:
        return target_info_cache[chembl_id]

    try:
        res = new_client.target.get(chembl_id, format='json')
        if not res:
            info = {"uniprot_id": "N/A", "target_name": "Unknown"}
        else:
            target_name = res.get('pref_name', 'Unknown')
            uniprot_id = res.get('target_components', [])[0].get("accession", "N/A")
            info = {"uniprot_id": uniprot_id, "target_name": target_name}
    except Exception as e:
        info = {"uniprot_id": f"Error: {str(e)[:50]}", "target_name": "Error"}

    target_info_cache[chembl_id] = info
    return info


def load_resources():
    global model, scaler, tokenizer, chembert_model, target_cols, target_info_cache

    print("🔄 Загрузка модели...")
    try:
        state_dict = torch.load("drug_prediction_model.pth", map_location=torch.device('cpu'))
        if isinstance(state_dict, dict):
            model = DrugPredictionModel()
            model.load_state_dict(state_dict)
        else:
            model = state_dict
        model.eval()
        print("✅ Модель загружена")
    except Exception as e:
        raise RuntimeError(f"❌ Не удалось загрузить модель: {e}")

    print("🔄 Загрузка scaler...")
    try:
        scaler = joblib.load("scaler.pkl")
        print("✅ Scaler загружен")
    except Exception as e:
        raise RuntimeError(f"❌ Не удалось загрузить scaler: {e}")

    print("🔄 Загрузка ChemBERT...")
    try:
        chembert_model_name = "seyonec/ChemBERTa-zinc-base-v1"
        tokenizer = AutoTokenizer.from_pretrained(chembert_model_name)
        chembert_model = AutoModel.from_pretrained(chembert_model_name)
        print("✅ ChemBERT загружен")
    except Exception as e:
        raise RuntimeError(f"❌ Не удалось загрузить ChemBERT: {e}")

    print("🔄 Загрузка имён мишеней...")
    dataset = pd.read_csv("drug_target_dataset.csv")
    target_cols = [col for col in dataset.columns if col not in ["compound_chembl_id", "smiles"]]
    print(f"✅ Найдено {len(target_cols)} мишеней")


    print("✅ Информация о мишениях будет загружаться по требованию (on-demand).")
    target_info_cache = {}

def get_morgan_fingerprint(smiles: str, radius=2, n_bits=2048) -> Optional[np.ndarray]:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    try:
        morgan_gen = GetMorganGenerator(
            radius=radius,
            fpSize=n_bits,
            includeChirality=False,
            useBondTypes=True,
            includeRingMembership=True,
            includeRedundantEnvironments=False
        )
        fp = morgan_gen.GetFingerprint(mol)
        return np.array(fp, dtype=np.float32)
    except Exception:
        return None

def get_chembert_embedding(smiles: str) -> Optional[np.ndarray]:
    global tokenizer, chembert_model
    try:
        inputs = tokenizer(smiles, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = chembert_model(**inputs)
        emb = outputs.last_hidden_state.mean(dim=1).detach().numpy().flatten()
        return emb.astype(np.float32)
    except Exception:
        return None

async def lifespan(_):
    load_resources()
    yield

app = FastAPI(
    title="Drug Target Predictor",
    lifespan=lifespan,
    description="API для предсказания биологической активности соединений по SMILES",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SmilesRequest(BaseModel):
    smiles: str

@app.post("/predict")
async def predict(request: SmilesRequest):
    global model, scaler, target_cols, target_info_cache

    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Модель не загружена")

    morgan_fp = get_morgan_fingerprint(request.smiles)
    chembert_emb = get_chembert_embedding(request.smiles)

    if morgan_fp is None:
        raise HTTPException(status_code=400, detail="Невалидный SMILES: не удалось сгенерировать Morgan fingerprint")
    if chembert_emb is None:
        raise HTTPException(status_code=400, detail="Невалидный SMILES: не удалось сгенерировать ChemBERT embedding")

    features = np.concatenate([morgan_fp, chembert_emb]).reshape(1, -1)
    try:
        features_norm = scaler.transform(features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка нормализации: {e}")

    try:
        with torch.no_grad():
            pred_tensor = model(torch.tensor(features_norm, dtype=torch.float32))
            pred_probs = pred_tensor.numpy().flatten()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка предсказания: {e}")

    results = []
    for i, chembl_id in enumerate(target_cols):
        if i >= len(pred_probs):
            break
        chance = float(pred_probs[i])
        info = get_uniprot_from_chembl(chembl_id)
        results.append({
            "chembl_id": chembl_id,
            "uniprot_id": info["uniprot_id"],
            "target_name": info["target_name"],
            "chance": round(chance, 4)
        })
    results.sort(key=lambda x: x["chance"], reverse=True)
    results = results[:10]

    return {"table": results}


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8001)
