import os
import sys
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Data.data_processor import DataManager


class RainfallPredictor:


    def __init__(self):
        self.dm = DataManager()
        self.scaler = StandardScaler()
        self.model = RandomForestRegressor(
            n_estimators=300,
            max_depth=20,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )

        self.city_encoder = LabelEncoder()
        self.metrics = {}
        self.is_trained = False

        self._train()

    def _train(self):
        df = self.dm.get_training_data()
        if df.empty:
            print("[ML] Training aborted: empty dataset")
            return

        # Time features
        df["time"] = pd.to_datetime(df["time"])
        df["month"] = df["time"].dt.month
        df["hour"] = df["time"].dt.hour

        # Remove extreme rainfall outliers
        df = df[df["rain"] < 100]

        # --- DATA BALANCING (OVERSAMPLING) ---
        # Yağış olan verileri çoğaltarak modelin öğrenmesini sağlıyoruz
        rainy_data = df[df["rain"] > 0]
        df = pd.concat([df, rainy_data, rainy_data, rainy_data, rainy_data, rainy_data], ignore_index=True)

        # Encode city as numeric feature
        df["city_encoded"] = self.city_encoder.fit_transform(df["city"])

        features = [
            "temperature", "humidity", "cloud_cover",
            "pressure", "wind_speed", "month", "hour", "city_encoded"
        ]

        X = df[features]
        y = df["rain"]

        # --- FEATURE SCALING ---

        X_scaled = self.scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        print("[ML] Training RandomForestRegressor with Scaled Data...")
        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)

        # Metrics calculation
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)

        y_test_binary = (y_test > 0.1).astype(int)
        pred_binary = (predictions > 0.1).astype(int)
        acc = accuracy_score(y_test_binary, pred_binary)

        self.metrics = {
            "MAE": f"{round(mae, 3)} mm",
            "RMSE": f"{round(rmse, 3)} mm",
            "R2": round(r2, 3),
            "Accuracy": f"{round(acc * 100, 2)}%"
        }

        self.is_trained = True
        print(f"[ML] Training completed → {self.metrics}")


    def predict_live(self, override_month=None):
        if not self.is_trained:
            return 0.0, self.metrics

        input_df = self.dm.get_live_data_for_prediction()
        if input_df.empty:
            return 0.0, self.metrics


        if override_month is not None:
            input_df["month"] = int(override_month)

        input_df["city_encoded"] = self.city_encoder.transform(input_df["city"])

        features = [
            "temperature", "humidity", "cloud_cover",
            "pressure", "wind_speed", "month", "hour", "city_encoded"
        ]

        # Ölçeklendirme ve tahmin
        X_live_scaled = self.scaler.transform(input_df[features])
        value = self.model.predict(X_live_scaled)[0]

        return round(max(0.0, value), 2), self.metrics