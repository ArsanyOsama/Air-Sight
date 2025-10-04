"""
process_merge.py
Merge latest datasets from ./data into a single features.parquet
for ML training.
"""

import os
import glob
import pandas as pd
import xarray as xr
from datetime import datetime

# -------------------------
# Helpers
# -------------------------
def latest_file(path, ext="*"):
    files = glob.glob(os.path.join(path, f"*.{ext}"))
    return max(files, key=os.path.getctime) if files else None

def load_csv(path):
    f = latest_file(path, "csv")
    return pd.read_csv(f) if f else pd.DataFrame()

def load_nc_or_zarr(path):
    f_nc = latest_file(path, "nc4")
    f_zarr = latest_file(path, "zarr")
    if f_nc:
        return xr.open_dataset(f_nc)
    if f_zarr:
        return xr.open_zarr(f_zarr, consolidated=False)
    return None

# -------------------------
# Load sources
# -------------------------
print("🚀 Loading datasets...")

# Ground truth (OpenAQ + AirNow)
openaq = load_csv("./data/openaq")
airnow = load_csv("./data/airnow")

# NASA (xarray datasets)
tempo = load_nc_or_zarr("./data/tempo")
merra2 = load_nc_or_zarr("./data/merra2")
imerg = load_nc_or_zarr("./data/imerg")
daymet = load_nc_or_zarr("./data/daymet")

# WHO & Pandora (static context)
who = load_csv("./data/who")
pandora = load_csv("./data/pandora")

# -------------------------
# Merge into feature set
# -------------------------
features = pd.DataFrame()

# Ground truth → PM2.5 / NO2
if not openaq.empty:
    features["pm25"] = openaq.get("value", pd.Series(dtype=float))
    features["parameter"] = openaq.get("parameter", pd.Series(dtype=str))
elif not airnow.empty:
    features["pm25"] = airnow.get("Value", pd.Series(dtype=float))
    features["parameter"] = airnow.get("Parameter", pd.Series(dtype=str))

# TEMPO variables
if tempo is not None:
    for v in ["NO2", "HCHO", "O3", "AI", "SO2"]:
        if v in tempo:
            features[v.lower()] = tempo[v].mean(dim=["lat","lon"]).to_pandas()

# MERRA-2 vars
if merra2 is not None:
    for v in ["PBLH","U10M","V10M","T2M","QV2M"]:
        if v in merra2:
            features[v.lower()] = merra2[v].mean(dim=["lat","lon"]).to_pandas()

# IMERG rainfall
if imerg is not None and "precipitationCal" in imerg:
    features["precip"] = imerg["precipitationCal"].mean(dim=["lat","lon"]).to_pandas()

# Daymet climatology
if daymet is not None:
    if "tmax" in daymet:
        features["daymet_tmax"] = daymet["tmax"].mean(dim=["lat","lon"]).to_pandas()

# WHO context
if not who.empty and "pm25_limit" in who:
    features["who_limit"] = who["pm25_limit"].iloc[0]

# Pandora ozone validation
if not pandora.empty and "ozone" in pandora:
    features["pandora_ozone"] = pandora["ozone"].iloc[0]

# -------------------------
# Save merged features
# -------------------------
os.makedirs("./data/processed", exist_ok=True)
out_file = f"./data/processed/features_{datetime.utcnow().date()}.parquet"
features.to_parquet(out_file, index=False)

print(f"✅ Features merged and saved → {out_file}")
