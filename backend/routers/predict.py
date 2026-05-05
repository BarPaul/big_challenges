from models.predict import PredictionRequest, PredictionResponse, TargetResult, ReportRequest
from fastapi import APIRouter, HTTPException, responses
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from textwrap import wrap
from httpx import AsyncClient
from dotenv import load_dotenv, find_dotenv
from os import getenv
from pathlib import Path
from uuid import uuid4
import csv


load_dotenv(find_dotenv())
router = APIRouter(prefix="/predict")
AI_SERVICE_URL = getenv("AI_SERVICE_URL", "http://0.0.0.0:8001")


@router.post("/biotargets", response_model=PredictionResponse)
async def predict_biotargets(request: PredictionRequest):
    async with AsyncClient() as client:
        try:
            response = await client.post(f"{AI_SERVICE_URL}/predict", json={"smiles": request.smiles})
            response.raise_for_status()
            data = response.json()
            filename = str(uuid4())

            table: list[TargetResult] = []
            for item in data.get("table", []):
                table.append(TargetResult(
                    chembl_id=item.get("chembl_id", ""),
                    uniprot_id=item.get("uniprot_id", "N/A"),
                    target_name=item.get("target_name", "Unknown"),
                    chance=float(item.get("chance", 0.0))
                ))

            base_path = Path("reports") / filename

            # TXT
            with open(base_path.with_suffix(".txt"), "w", encoding="utf-8") as f:
                f.write("Результаты предсказания биомишеней\n")
                f.write("-" * 50 + "\n")
                for i, tr in enumerate(table, 1):
                    f.write(f"{i}. {tr.chembl_id} | {tr.target_name} | UniProt: {tr.uniprot_id} | P = {tr.chance:.3f}\n")

            # CSV
            with open(base_path.with_suffix(".csv"), "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["ChEMBL", "UniProt", "Target", "Probability"])
                writer.writeheader()
                for tr in table:
                    writer.writerow({
                        "ChEMBL": tr.chembl_id,
                        "UniProt": tr.uniprot_id,
                        "Target": tr.target_name,
                        "Probability": f"{tr.chance:.4f}"
                    })

            # PDF
            c = canvas.Canvas(str(base_path.with_suffix(".pdf")), pagesize=A4)
            _, height = A4

            c.drawString(2*cm, height - 2*cm, "Prediction result")
            y = height - 3.5*cm

            for tr in table:
                line = f"{tr.chembl_id}: {tr.target_name} (UniProt: {tr.uniprot_id}) — P: {tr.chance:.3f}"
                wrapped_lines = wrap(line, width=80)

                for wrapped_line in wrapped_lines:
                    if y < 2*cm:
                        c.showPage()
                        y = height - 2*cm
                    c.drawString(2*cm, y, wrapped_line)
                    y -= 1.2*cm

            c.save()


            return PredictionResponse(id=filename, table=table)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка AI сервиса: {str(e)}")

@router.post("/download", response_class=responses.FileResponse)
async def download_report(request: ReportRequest):
    file_path = Path("reports") / f"{request.id}.{request.extension}"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Отчёт не найден.")

    if request.extension not in ("txt", "csv", "pdf"):
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат")

    return responses.FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=f"report_{request.id}.{request.extension}"
    )
