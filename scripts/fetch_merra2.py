import xarray as xr

def fetch_merra2():
    url = "s3://nasanex/MERRA2/daily.zarr"  # Example, replace with actual MERRA-2 zarr
    ds = xr.open_zarr(url, consolidated=True, storage_options={"anon": True})
    ds_subset = ds[["T2M","QV2M","U10M","V10M","PBLH"]].isel(time=slice(-1, None))
    ds_subset.to_zarr("data/merra2.zarr", mode="w")
    print("✅ Saved latest MERRA-2 slice to data/merra2.zarr")

if __name__ == "__main__":
    fetch_merra2()
