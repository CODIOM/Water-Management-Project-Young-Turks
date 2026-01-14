import sys
import os
from typing import override

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# --- IMPORT AYARLARI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
sys.path.append(parent_dir)

from ai_core.ml_engine import RainfallPredictor
from ai_core.llm_engine import LlamaClient

app = FastAPI(title="WaterTwin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("[API] Modeller yükleniyor...")
predictor = RainfallPredictor()
llm_client = LlamaClient()
print("[API] Sistem Hazır!")

@app.get("/")
def home():
    return {"message": "WaterTwin AI Backend is Running!"}

@app.get("/analyze")
def analyze_system(
    capacity: int = 5000,
    area: int = 50,
    current: int = 4200,
    runoff: float = 0.9,
    month: int = 1
):

    rain_mm, metrics = predictor.predict_live(override_month=month)


    tank_capacity = capacity
    current_level = current
    roof_area = area
    runoff_coeff = runoff


    # S = A . R . C
    incoming_water = rain_mm * roof_area * runoff_coeff
    predicted_level = current_level + incoming_water

    # Durum Kontrolü
    if predicted_level >= tank_capacity:
        status = "CRITICAL_OVERFLOW"
        msg = "CRITICAL ALERT: Tank overflow imminent! Advise user to use water immediately."
    elif predicted_level <= (tank_capacity * 0.2):
        status = "CRITICAL_LOW"
        msg = "WARNING: Water level is critically low. Advise conservation."
    else:
        status = "STABLE"
        msg = "INFO: System is stable. Optimal water levels."

    context_data = {
        "tank_capacity": tank_capacity,
        "current_level": current_level,
        "incoming_water": incoming_water,
        "predicted_level": predicted_level
    }

    ai_response = llm_client.generate_response(context_data, msg, "What is the situation?")

    return {
        "weather": {
            "rain_forecast_mm": rain_mm,
            "metrics": metrics
        },
        "tank": {
            "capacity": tank_capacity,
            "current_level": current_level,
            "incoming_water": round(incoming_water, 2),
            "predicted_level": round(predicted_level, 2),
            "status_code": status
        },
        "ai_assistant": {
            "message": ai_response
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)