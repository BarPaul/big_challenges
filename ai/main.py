from uvicorn import run
from fastapi import FastAPI
from pydantic import BaseModel
from model import load_model, predict_targets


app = FastAPI(
    title="AI Inference Service",
    on_startup=load_model
)


class InferenceRequest(BaseModel):
    smiles: str


@app.post("/infer")
async def infer(request: InferenceRequest):
    return {"table": predict_targets(request.smiles)}


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8001)
