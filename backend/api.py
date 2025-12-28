import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# --- IMPORT AYARLARI (AI Core'u bulması için) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
sys.path.append(parent_dir)

from ai_core.ml_engine import RainfallPredictor
from ai_core.llm_engine import LlamaClient

# --- UYGULAMA BAŞLANGICI ---
app = FastAPI(title="WaterTwin API")

# CORS (Frontend'in bu API'ye erişmesine izin ver)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelleri Başlat (Sunucu açılırken bir kere yüklenir)
print("🚀 [API] Modeller yükleniyor...")
predictor = RainfallPredictor()
llm_client = LlamaClient()
print("✅ [API] Sistem Hazır!")


@app.get("/")
def home():
    return {"message": "WaterTwin AI Backend is Running!"}


@app.get("/analyze")
def analyze_system():
    """
    Bu endpoint çağrıldığında:
    1. Hava durumunu tahmin eder.
    2. Su deposu simülasyonu yapar.
    3. LLM'den rapor alır.
    4. Tüm veriyi JSON olarak döner.
    """
    # 1. TAHMİN
    rain_mm, metrics = predictor.predict_live()

    # 2. SİMÜLASYON (Varsayılan Senaryo)
    tank_capacity = 5000
    current_level = 4200  # Örnek: Depo %84 dolu
    roof_area = 50  # 50 m2 çatı

    incoming_water = rain_mm * roof_area * 0.9  # %90 verimlilik
    predicted_level = current_level + incoming_water

    # Taşma Kontrolü
    if predicted_level > tank_capacity:
        status = "CRITICAL_OVERFLOW"
        msg = "CRITICAL ALERT: Tank overflow imminent! Advise user to use water immediately."
    elif predicted_level < (tank_capacity * 0.2):
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

    # 3. LLM RAPORU
    # Not: Hız için LLM'i opsiyonel yapabilirsin ama şimdilik kalsın.
    ai_response = llm_client.generate_response(context_data, msg, "What is the situation?")

    # 4. JSON CEVAP
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
    # Dosyayı direkt çalıştırırsan sunucuyu başlatır
    uvicorn.run(app, host="127.0.0.1", port=8000)