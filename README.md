🌍 AirSight NASA — Predicting Cleaner, Safer Skies


<img width="1280" height="626" alt="image" src="https://github.com/user-attachments/assets/22aa7f90-0bab-4ea0-92b2-99d93c14a0b8" />


🚀 Built for NASA Space Apps Challenge 2025 (Cairo)
AirSight integrates NASA Earth Observations, ground sensors, and AI to forecast air quality, deliver alerts, and empower healthier communities.

✨ Problem

Air pollution kills 7M people annually (WHO). Cairo, like many cities, faces:

High NO₂ and PM₂.₅ from traffic & industry

Seasonal pollution traps (low winds, high humidity)

Lack of accessible real-time forecasts

Communities need science-driven, actionable insights to make safer daily decisions.

🌐 Our Solution — AirSight

<img width="744" height="697" alt="image" src="https://github.com/user-attachments/assets/8f346787-7f6d-4f4d-a667-5c7918633292" />



✅ Data-driven forecasts combining NASA satellites + ground truth
✅ AI model predicting PM₂.₅ & AQI hourly/daily
✅ Visual dashboards with NASA overlays (NO₂, SO₂ hotspots)
✅ Citizen alerts via Firebase/WebSockets
✅ Explainable AI → SHAP explains what drives poor air

🛰️ Data Sources
Source	Variables	Format	Refresh
NASA TEMPO	NO₂, SO₂, O₃, HCHO, Aerosol Index	NetCDF/HDF	Daily (NRT)
MERRA-2	Winds, Temp, Humidity, PBL Height	Zarr/NetCDF	Daily
IMERG (GPM)	Rainfall (pollutant washout)	NetCDF/Zarr	30 min–Daily
NASA GIBS	NO₂/SO₂ satellite overlays	WMTS tiles (PNG)	On-demand
OpenAQ	PM₂.₅, NO₂ ground truth	REST API (JSON)	Hourly
AirNow	AQI backup	REST API (JSON/XML)	Hourly
Daymet	Climate (temperature trends)	NetCDF/CSV	Static
WHO	Health context	CSV/Excel	Static
Pandora/TOLNet	Ozone validation	CSV	Optional

📌 Design Choice: We only store slices (hour/day, region of interest), not TBs of global data → efficient, hackathon-friendly, scalable.

🔗 Pipeline Architecture
flowchart TD
    A[NASA TEMPO, MERRA-2, IMERG] -->
    B[Preprocessing (xarray/dask)]
    C[OpenAQ / AirNow APIs] --> B
    D[Daymet, WHO, Pandora] --> B
    B --> E[Feature Store (Parquet/CSV)]
    E --> F[ML Training (XGBoost, SHAP)]
    F --> G[FastAPI Backend (/forecast)]
    G --> H[Frontend (React + Mapbox + Firebase Alerts)]
    H --> I[Citizens / Policymakers]

⚡ Tech Stack

Data Engineering

earthaccess, xarray, zarr, netCDF4, pandas

requests (API ingestion)

n8n (automation scheduler, hourly/daily flows)

Machine Learning

XGBoost, scikit-learn

SHAP (explainable AI)

Backend

FastAPI, Uvicorn

WebSockets (real-time streaming)

Frontend

React, Mapbox, Tailwind

Firebase (citizen alerts)

🚦 Features

🌍 Global & Local Data Access

🏙️ Hourly AQ Forecasts (PM₂.₅, AQI, NO₂)

🛰️ NASA Satellite Maps (NO₂/SO₂ hotspots via GIBS)

🚨 Citizen Alerts (high-risk groups via Firebase)

📊 Explainable Predictions (SHAP)

🧩 Modular Pipeline (easy to extend with new datasets)
