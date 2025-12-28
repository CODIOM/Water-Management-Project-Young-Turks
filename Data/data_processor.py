import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta


class DataManager:
    """
    Responsible for:
    - Downloading historical weather data
    - Saving/loading CSV files
    - Providing live data for prediction
    """

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.history_csv_path = os.path.join(self.base_dir, "historical_hourly_data.csv")

        # Default live prediction location (Istanbul)
        self.lat = 41.0082
        self.lon = 28.9784

    def get_training_data(self):
        """
        Load training data from CSV if exists,
        otherwise download from Open-Meteo archive.
        """
        if os.path.exists(self.history_csv_path):
            print("✅ [Data] Loading historical data from CSV")
            return pd.read_csv(self.history_csv_path)

        return self._download_historical_data()

    def _download_historical_data(self):
        """
        Download last 3 years of hourly weather data
        for multiple nearby cities to improve generalization.
        """
        print("🌍 [Data] Downloading 3 years of hourly weather data...")

        locations = [
            {"city": "Istanbul", "lat": 41.0082, "lon": 28.9784},
            {"city": "Bursa", "lat": 40.1826, "lon": 29.0662},
            {"city": "Izmir", "lat": 38.4192, "lon": 27.1287},
            {"city": "Canakkale", "lat": 40.1553, "lon": 26.4142},
            {"city": "Tekirdag", "lat": 40.9833, "lon": 27.5167}
        ]

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=1095)

        base_params = {
            "start_date": start_date,
            "end_date": end_date,
            "hourly": (
                "temperature_2m,relative_humidity_2m,rain,"
                "surface_pressure,wind_speed_10m,cloud_cover"
            ),
            "timezone": "auto"
        }

        all_frames = []

        for loc in locations:
            try:
                params = base_params.copy()
                params["latitude"] = loc["lat"]
                params["longitude"] = loc["lon"]

                response = requests.get(
                    "https://archive-api.open-meteo.com/v1/archive",
                    params=params
                )
                data = response.json()

                if "hourly" not in data:
                    continue

                df = pd.DataFrame(data["hourly"])
                df["city"] = loc["city"]

                all_frames.append(df)
                print(f"⬇️ {loc['city']} data downloaded")

                time.sleep(0.5)

            except Exception as e:
                print(f"❌ Error downloading {loc['city']}: {e}")

        if not all_frames:
            return pd.DataFrame()

        full_df = pd.concat(all_frames, ignore_index=True)

        # Rename columns for consistency
        full_df = full_df.rename(columns={
            "temperature_2m": "temperature",
            "relative_humidity_2m": "humidity",
            "surface_pressure": "pressure",
            "wind_speed_10m": "wind_speed"
        })

        # Basic cleaning
        full_df["time"] = pd.to_datetime(full_df["time"])
        full_df = full_df.dropna()

        # Save locally
        full_df.to_csv(self.history_csv_path, index=False)
        print(f"✅ [Data] Saved {len(full_df)} rows to CSV")

        return full_df

    def get_live_data_for_prediction(self):
        """
        Fetch current weather conditions for live prediction.
        """
        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": self.lat,
                    "longitude": self.lon,
                    "current": (
                        "temperature_2m,relative_humidity_2m,"
                        "cloud_cover,pressure_msl,wind_speed_10m"
                    ),
                    "timezone": "auto"
                }
            )

            current = response.json().get("current", {})
            now = datetime.now()

            return pd.DataFrame([{
                "temperature": current.get("temperature_2m", 15),
                "humidity": current.get("relative_humidity_2m", 60),
                "cloud_cover": current.get("cloud_cover", 50),
                "pressure": current.get("pressure_msl", 1013),
                "wind_speed": current.get("wind_speed_10m", 10),
                "month": now.month,
                "hour": now.hour,
                "city": "Istanbul"
            }])

        except Exception as e:
            print(f"❌ [Data] Live data error: {e}")
            return pd.DataFrame()
