import sys
import os

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml_engine import RainfallPredictor
from llm_engine import LlamaClient


def run_system_test():
    print("=========================================")
    print("WATER TWIN AI - SYSTEM TEST")
    print("=========================================")

    # 1. ML ENGINE
    print("\n[1] Analyzing Weather Data...")
    predictor = RainfallPredictor()
    rain_mm, metrics = predictor.predict_live()

    print(f"\n   PREDICTED RAIN: {rain_mm} mm")


    print(f"   ACCURACY: {metrics.get('Accuracy', 'N/A')}")
    print(f"   ERROR MARGIN (MAE): {metrics.get('MAE', 'N/A')}")
    print(f"   R2 SCORE: {metrics.get('R2', 'N/A')}")

    # 2. LOGIC & SIMULATION
    current_level = 4800
    capacity = 5000
    incoming_water = rain_mm * 50  # 50m2 roof
    predicted_level = current_level + incoming_water

    # Status Logic in English
    if predicted_level > capacity:
        status_msg = "CRITICAL ALERT: Tank overflow imminent! Advise user to use water immediately."
    elif predicted_level < (capacity * 0.2):
        status_msg = "WARNING: Water level is critically low. Advise conservation."
    else:
        status_msg = "INFO: System is stable. Optimal water levels."

    context_data = {
        "tank_capacity": capacity,
        "current_level": current_level,
        "incoming_water": incoming_water,
        "predicted_level": predicted_level
    }

    # 3. LLM REPORT
    print("\n[2] Generating Assistant Report...")
    llm = LlamaClient()

    # Ensure llm_engine.py is also set to English as we did in the previous step
    answer = llm.generate_response(context_data, status_msg, "What is the status?")

    print(f"\n ASSISTANT RESPONSE:\n{answer}")


if __name__ == "__main__":
    run_system_test()