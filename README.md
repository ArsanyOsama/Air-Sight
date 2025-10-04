🌍 AirSight NASA — Clean Skies with AI + Earth Data

🚀 Built for NASA Space Apps Challenge 2025 (Cairo)
Harnessing NASA Earth Observations + AI to forecast cleaner and safer air.

✨ Overview

AirSight combines NASA satellite data, ground air-quality sensors, and machine learning to deliver real-time forecasts and citizen alerts for air quality (PM₂.₅, NO₂, AQI).

We integrate cloud-first pipelines, open APIs, and explainable AI to empower communities and policymakers with science-backed predictions.

🛰️ Data Sources
Source	Variables	Format	Refresh
NASA TEMPO	NO₂, SO₂, O₃, HCHO, Aerosol Index	NetCDF/HDF	Daily (NRT)
MERRA-2	Winds, Temp, Humidity, PBL Height	Zarr/NetCDF	Daily
IMERG (GPM)	Rainfall (pollutant washout)	NetCDF/Zarr	30 min–Daily
NASA GIBS	Satellite NO₂ maps	WMTS tiles (PNG)	On-demand
OpenAQ	PM₂.₅, NO₂ (ground truth)	REST API (JSON)	Hourly
AirNow	AQI backup	REST API (JSON/XML)	Hourly
Daymet	Climate (temp trends)	NetCDF/CSV	Static
WHO	Health context	CSV/Excel	Static
Pandora/TOLNet	Ozone validation	CSV	Optional
🔗 Pipeline Workflow
flowchart TD
    A[NASA TEMPO, MERRA-2, IMERG] --> B[Preprocessing (xarray/dask)]
    C[OpenAQ / AirNow] --> B
    D[Daymet, WHO, Pandora] --> B
    B --> E[Feature Store (Parquet/CSV)]
    E --> F[ML Training (XGBoost, SHAP)]
    F --> G[FastAPI Backend (/forecast)]
    G --> H[Frontend (React + Mapbox + Firebase Alerts)]
    H --> I[Citizens / Policymakers]

⚡ Tech Stack

Data Ingestion: earthaccess, requests, xarray, zarr, pandas

Automation: n8n (hourly + daily schedulers)

Storage: Local / Backblaze B2 (S3 API)

ML & Explainability: XGBoost, scikit-learn, SHAP

Backend: FastAPI, Uvicorn

Frontend: React, Mapbox, Firebase/WebSockets

🚦 Features

✅ Global & Local Data: NASA satellites + Cairo ground stations
✅ Hourly Forecasts: PM₂.₅ + AQI levels
✅ Daily Satellite Overlays: NASA GIBS maps (NO₂ hot spots)
✅ Explainable AI: SHAP explains drivers of pollution
✅ Citizen Alerts: Firebase/WebSockets → real-time warnings
✅ Scalable Pipeline: Cloud-ready
