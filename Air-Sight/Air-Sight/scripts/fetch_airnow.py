import requests, pandas as pd
from datetime import datetime, timedelta

API_KEY = "760804B0-495F-438A-ACF9-04A688DC6A11"

BASE_URL = "https://www.airnowapi.org/aq/data/"
PARAMS = {
    "startDate": (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%dT%H"),
    "endDate": datetime.utcnow().strftime("%Y-%m-%dT%H"),
    "parameters": "PM25,NO2,OZONE,SO2",
    "BBOX": "-180,-90,180,90",  # global coverage
    "dataType": "A",
    "format": "application/json",
    "API_KEY": API_KEY
}

def fetch_airnow():
    r = requests.get(BASE_URL, params=PARAMS)
    if r.status_code != 200:
        print("❌ No AirNow data returned", r.text)
        return
    data = r.json()
    df = pd.DataFrame(data)
    df.to_csv("data/airnow_measurements.csv", index=False)
    print(f"✅ Saved {len(df)} rows to data/airnow_measurements.csv")

if __name__ == "__main__":
    fetch_airnow()
