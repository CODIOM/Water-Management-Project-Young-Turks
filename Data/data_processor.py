import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

class DataManager:

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.history_csv_path = os.path.join(self.base_dir, "historical_hourly_data.csv")

        # Hedef Sadece İstanbul
        self.lat = 41.0082
        self.lon = 28.9784
        self.default_city = "Istanbul"

    def get_training_data(self):

        if os.path.exists(self.history_csv_path):
            print("[Data] 10 Yıllık İstanbul verisi CSV'den okunuyor...")
            return pd.read_csv(self.history_csv_path)

        return self._download_historical_data()

    def _download_historical_data(self):
        print("[Data] İstanbul için son 10 YILIN kritik parametreleri indiriliyor...")
        
        locations = [
            {"city": "Istanbul", "lat": 41.0082, "lon": 28.9784}
        ]
        
        # 10 Yıllık Veri
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=3650) 
        
        # API Parametreleri
        params_base = {
            "start_date": start_date,
            "end_date": end_date,
            "hourly": (
                "temperature_2m,relative_humidity_2m,dewpoint_2m,"
                "rain,surface_pressure,pressure_msl,"
                "wind_speed_10m,wind_direction_10m,cloud_cover"
            ),
            "timezone": "auto"
        }

        frames = []
        for loc in locations:
            try:
                p = params_base.copy()
                p["latitude"] = loc["lat"]
                p["longitude"] = loc["lon"]
                
                r = requests.get("https://archive-api.open-meteo.com/v1/archive", params=p)
                d = r.json()
                
                if "hourly" in d:
                    df = pd.DataFrame(d["hourly"])
                    df["city"] = loc["city"]
                    frames.append(df)
                    print(f"   {loc['city']} verisi indirildi (10 Yıllık).")
                
                time.sleep(1) 

            except Exception as e:
                print(f"   Hata ({loc['city']}): {e}")

        if not frames: return pd.DataFrame()
        
        full_df = pd.concat(frames, ignore_index=True)
        
        # --- İSİM DÜZELTME (Mapping) ---

        full_df = full_df.rename(columns={
            "temperature_2m": "temperature",
            "relative_humidity_2m": "humidity",
            "dewpoint_2m": "dew_point",
            "pressure_msl": "pressure",
            "wind_speed_10m": "wind_speed",
            "wind_direction_10m": "wind_dir",

        })
        

        if "surface_pressure" in full_df.columns:
            full_df = full_df.drop(columns=["surface_pressure"])

        full_df["time"] = pd.to_datetime(full_df["time"])
        full_df = full_df.dropna()
        
        full_df.to_csv(self.history_csv_path, index=False)
        print(f"[Data] Kaydedildi: {len(full_df)} satır.")
        return full_df

    def get_live_data_for_prediction(self):

        try:
            r = requests.get("https://api.open-meteo.com/v1/forecast", params={
                "latitude": self.lat, 
                "longitude": self.lon,
                "current": (
                    "temperature_2m,relative_humidity_2m,dewpoint_2m,"
                    "cloud_cover,pressure_msl,"
                    "wind_speed_10m,wind_direction_10m"
                ),
                "timezone": "auto"
            })
            c = r.json().get("current", {})
            n = datetime.now()
            
            return pd.DataFrame([{
                "temperature": c.get("temperature_2m", 15),
                "humidity": c.get("relative_humidity_2m", 60),
                "dew_point": c.get("dewpoint_2m", 10),
                "cloud_cover": c.get("cloud_cover", 50),
                "pressure": c.get("pressure_msl", 1013),
                "wind_speed": c.get("wind_speed_10m", 10),
                "wind_dir": c.get("wind_direction_10m", 180),
                "month": n.month,
                "hour": n.hour,
                "city": self.default_city
            }])
        except Exception as e:
            print(f"[Data] Canlı veri hatası: {e}")
            return pd.DataFrame()