#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
import joblib, os
import pandas as pd

# Always resolve config.json from project root
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # go up from scripts/
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

app = FastAPI(title="AirQuality Forecast API")

MODEL_KEY = "models/xgb_v1.joblib"
LOCAL_MODEL_PATH = "/tmp/xgb_v1.joblib"

# Load model at startup
try:
    model = joblib.load(LOCAL_MODEL_PATH)
except Exception:
    model = None

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": bool(model)}

@app.get("/forecast")
def forecast(lat: float = None, lon: float = None, station_id: str = None):
    """
    Simple stub:
    - If station_id provided, look up in processed features and return last known prediction.
    - Else: return error (implement dynamic feature extraction for full app).
    """
    if not model:
        raise HTTPException(status_code=503, detail="Model not available")
    if station_id:
        # Placeholder for local file-based implementation
        raise HTTPException(status_code=501, detail="Feature not implemented for local files")
    else:
        raise HTTPException(status_code=400, detail="Provide station_id")