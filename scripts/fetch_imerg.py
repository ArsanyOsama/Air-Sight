import earthaccess, xarray as xr, os
from datetime import datetime

os.makedirs("./data/imerg", exist_ok=True)

def fetch_imerg():
    auth = earthaccess.login(persist=True)
    results = earthaccess.search_data(
        short_name="GPM_3IMERGHHE",
        bounding_box=(25,22,36,32),
        temporal=(str(datetime.utcnow().date()), str(datetime.utcnow().date()))
    )
    if not results:
        print("❌ No IMERG files")
        return
    file = earthaccess.download(results[0])
    ds = xr.open_dataset(file)
    out = f"./data/imerg/{datetime.utcnow().date()}.zarr"
    ds.to_zarr(out, mode="w")
    print(f"✅ IMERG saved → {out}")

if __name__ == "__main__":
    fetch_imerg()
