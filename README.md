<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

<img src="codiom.jpeg" width="180px" alt="" style="margin-bottom: 10px;"/>

# <code>DIGITAL TWIN–BASED RAINWATER MANAGEMENT SYSTEM</code>

<em>Young Turks</em>

<!-- BADGES -->
<!-- local repository, no metadata badges. -->

<em>Target Technologies:</em>

<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/Flask-000000.svg?style=for-the-badge&logo=Flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/Digital_Twin_Modeling-1E90FF.svg?style=for-the-badge&logo=Unity&logoColor=white" alt="DigitalTwin">
<img src="https://img.shields.io/badge/TimeSeries_DB-FF6F00.svg?style=for-the-badge&logo=InfluxDB&logoColor=white" alt="InfluxDB">
<img src="https://img.shields.io/badge/FAISS-00B0FF.svg?style=for-the-badge&logo=Facebook&logoColor=white" alt="FAISS">
<img src="https://img.shields.io/badge/scikit--learn-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn">
<img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=for-the-badge&logo=HTML5&logoColor=white" alt="HTML5">
<img src="https://img.shields.io/badge/CSS3-1572B6.svg?style=for-the-badge&logo=CSS3&logoColor=white" alt="CSS3">
<img src="https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white" alt="Docker">


</div>
<br>

---

##  Table of Contents
- [ Overview](#️-overview)
- [ Team](#-team)
- [ Problem](#-problem)
- [ Solution](#-solution)
- [ Key Features](#-key-features)
- [ Tech Stack](#-tech-stack)
- [ System Architecture](#️-system-architecture)
- [ Data Sources](#-data-sources)
- [ Roadmap](#️-roadmap)
---

##  Overview
**WaterTwin AI** is a **fully predictive** Digital Twin platform for urban water management. Instead of relying on physical sensors, the system uses **meteorological forecasts, historical rainfall data, and mathematical models** to simulate water accumulation, predict tank levels, and analyze flood risks in a virtual environment.

##  Team

| Role | Member | LinkedIn |
|------|--------|-----------|
| **Data Modeling** | Berat Erol Çelik | [![LinkedIn](https://img.shields.io/badge/-Berat_Erol_Çelik-0077B5?style=flat-square&logo=LinkedIn&logoColor=white)](https://www.linkedin.com/in/berat-erol-%C3%A7elik-513915258/) |
| **Backend & API** | Emre Aldemir | [![LinkedIn](https://img.shields.io/badge/-Emre_Aldemir-0077B5?style=flat-square&logo=LinkedIn&logoColor=white)](https://www.linkedin.com/in/emre-aldemir-1b2301293/) |
| **Frontend & UI/UX Dashboard** | Umut Odabaş | [![LinkedIn](https://img.shields.io/badge/-Umut_Odabaş-0077B5?style=flat-square&logo=LinkedIn&logoColor=white)](https://www.linkedin.com/in/umut-odaba%C5%9F-8a26142a2/) |
| **Machine Learning (Forecasting & Simulation)** | Ömer Altıntaş | [![LinkedIn](https://img.shields.io/badge/-Ömer_Altıntaş-0077B5?style=flat-square&logo=LinkedIn&logoColor=white)](https://www.linkedin.com/in/%C3%B6mer-alt%C4%B1nta%C5%9F-44773730b/) |

---

##  Problem
Cities struggle with unpredictable rainfall and inefficient water collection planning.
Current limitations:
- Lack of foresight into how much water *will* be collected during a storm.
- Inability to simulate storage capacity without installing expensive hardware.
- Difficulty in planning "what-if" scenarios (e.g., "If it rains 50mm, will our tanks overflow?").
- Reactive approaches rather than proactive, data-driven planning.---

##  Solution

**WaterTwin AI**
A purely software-based Digital Twin platform that:
- **Predicts** incoming rainwater volume based on weather APIs and catchment area calculations.
- **Simulates** tank fill levels mathematically without physical sensors.
- **Optimizes** water usage by forecasting future availability.
- **Visualizes** potential flood risks and overflow scenarios on a digital map.

---

##  Key Features

| Feature | Description | Status |
|---------|-------------|---------|
|  **Rainfall Prediction** | ML model forecasts rainfall (mm) for next hours/days | ❌ Planning |
|  **Virtual Catchment Model** | Calculates water volume based on roof area & runoff coef. | ❌ Planning |
|  **Predictive Simulation** | Simulates tank levels based on predicted inflow vs. usage | ❌ Planning |
|  **Overflow Forecasting** | Predicts when tanks will reach capacity *before* it rains | ❌ Planning |
|  **Interactive Dashboard** | Visualization of predicted data and simulation results | ❌ Planning |
|  **Scenario Analysis** | Simulation of extreme weather events (Drought/Flood) | ❌ Planning |
|  **Strategic Planning** | Long-term water availability reports | ❌ Planning |

---

##  Tech Stack

### Backend & API
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/FastAPI-009688.svg?style=for-the-badge&logo=FastAPI&logoColor=white"> <img src="https://img.shields.io/badge/Flask-000000.svg?style=for-the-badge&logo=Flask&logoColor=white">

### Artificial Intelligence & Simulation
<img src="https://img.shields.io/badge/scikit--learn-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white"> <img src="https://img.shields.io/badge/PyTorch-EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white"> <img src="https://img.shields.io/badge/NumPy-4B8BBE.svg?style=for-the-badge&logo=NumPy&logoColor=white"> <img src="https://img.shields.io/badge/Pandas-150458.svg?style=for-the-badge&logo=Pandas&logoColor=white">

### Frontend
<img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white"> <img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=for-the-badge&logo=HTML5&logoColor=white"> <img src="https://img.shields.io/badge/CSS3-1572B6.svg?style=for-the-badge&logo=CSS3&logoColor=white">

### Database & Deployment
<img src="https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white"> <img src="https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white"> <img src="https://img.shields.io/badge/Render-46E3B7.svg?style=for-the-badge&logo=Render&logoColor=white">

---

## System Architecture

The system acts as a real-time digital twin that models rainfall, water flow, storage tanks, and distribution lines.

```sh
└── /
    ├── ai_models
    │   ├── weather_forecasting  # Predicts rainfall
    │   ├── runoff_calculator    # Calculates water volume
    │   └── consumption_model    # Estimates water usage
    ├── backend
    │   └── api
    ├── data
    │   ├── historical_weather
    │   └── system_parameters    # Roof size, tank capacity etc.
    ├── deployment
    │   └── docker
    ├── docs
    │   └── mathematical_models
    └── frontend
        ├── ui
        └── charts
```

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/predict/rain` | GET | Returns ML-based rainfall forecast for the location |
| `/api/simulate/tank` | POST | Calculates expected tank level based on forecasted rain |
| `/api/simulate/scenario` | POST | Runs a "What-if" scenario (e.g., heavy storm simulation) |
| `/api/report/capacity` | GET | Returns predicted water availability for the next week |

### Data Flow
1. **Input**: System fetches weather forecast (Rainfall in mm) and user inputs (Catchment area in m²).
2. **Calculation**: Volume (L) = Rainfall (mm) × Area (m²) × Runoff Coefficient.
3. **Prediction**: ML Model adjusts for evaporation and historical consumption patterns.
4. **Simulation**: The Digital Twin updates the virtual tank levels.
5. **Decision**: If Predicted Level > Tank Capacity, the system issues an overflow warning.

---

##  Data Sources

Since there are no physical sensors, the system relies on high-quality external data:

OpenWeatherMap API / MGM - Source for real-time and forecasted weather data.

Historical Climate Data - Used to train the ML prediction models.

User-Defined Infrastructure Data - Roof area dimensions, tank capacities, and water usage estimates.

##  Roadmap
-  **`Task 1`**: Algorithm Design (Rainfall-to-Volume Conversion)
-  **`Task 2`**: Integration with Weather APIs
-  **`Task 3`**: Development of Prediction Models (ML)
-  **`Task 4`**: Building the Digital Twin Simulation Logic
-  **`Task 5`**: Dashboard for Visualization of Predictions
-  **`Task 6`**: Scenario Testing & Reporting


**Technologies:**  
- Python 3.x  
- Flask / FastAPI  
- Scikit-learn (For regression/time-series forecasting)
- Pandas (For data manipulation)
- Streamlit (For visualization)

---

### Example Data Flow

1. Forecast: Weather API predicts 40mm of rain for tomorrow.
2. System Config: Building has a 500m² roof and a 15,000L tank (currently estimated at 50% full).
3. Calculation: 40mm × 500m² × 0.9 (efficiency) = 18,000 Liters of potential harvest.
4. Simulation: Current water (7,500L) + Inflow (18,000L) = 25,500L.
5. Outcome: Since 25,500L > 15,000L (Capacity), the system predicts an Overflow of 10,500L.
6. Advice: "Recommended Action: Use stored water for irrigation today to create space."

---


[![][back-to-top]](#top)

</div>


[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square


---
















