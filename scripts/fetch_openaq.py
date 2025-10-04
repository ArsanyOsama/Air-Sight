import requests, os
from datetime import datetime, timedelta
import pandas as pd

BASE_URL = "https://api.openaq.org/v3/measurements"

params = {
    "limit": 5,
    "parameter": "pm25,no2",
    "date_from": (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d"),
    "date_to": datetime.utcnow().strftime("%Y-%m-%d")
}

print("Requesting:", BASE_URL, "with params:", params)
resp = requests.get(BASE_URL, params=params)
print("Status:", resp.status_code)
print("Response body:", resp.text[:200])

if resp.status_code == 200:
    data = resp.json().get("results", [])
    if data:
        df = pd.json_normalize(data)
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/openaq_test.csv", index=False)
        print("✅ Wrote test CSV with rows:", len(df))
    else:
        print("⚠️ No results in ‘results’")
else:
    print("❌ Request error", resp.status_code)