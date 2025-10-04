import earthaccess, xarray as xr, os
from datetime import datetime


os.makedirs("./data/tempo", exist_ok=True)

def fetch_tempo():
    auth = earthaccess.login(persist=True)
    results = earthaccess.search_data(
        short_name="TEMPO_NO2_L2",
        bounding_box=(25,22,36,32),   # Egypt
        temporal=(str(datetime.utcnow().date()), str(datetime.utcnow().date()))
    )
    if not results:
        print("❌ No TEMPO files found")
        return
    file = earthaccess.download(results[0])
    ds = xr.open_dataset(file)
    out = f"./data/tempo/{datetime.utcnow().date()}.zarr"
    ds.to_zarr(out, mode="w")
    print(f"✅ TEMPO saved → {out}")

if __name__ == "__main__":
    fetch_tempo()
