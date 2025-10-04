#!/usr/bin/env python3
"""
train_model.py
- Load features Parquet from B2 (processed/features_*.parquet)
- Train a simple XGBoost regressor (predict next-24h mean PM2.5)
- Save model to models/xgb_v1.joblib and upload to B2
"""
import json, os, joblib, logging
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBRegressor
from botocore.client import Config
import boto3

cfg = json.load(open("config.json"))
s3cfg = cfg["s3"]
BUCKET = s3cfg["bucket"]

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("train_model")

def download_latest_features():
    import s3fs
    fs = s3fs.S3FileSystem(key=s3cfg["access_key"], secret=s3cfg["secret_key"],
                           client_kwargs={"endpoint_url": s3cfg.get("endpoint_url")})
    files = fs.glob(f"{BUCKET}/processed/features/*")
    if not files:
        LOG.error("No processed features in bucket")
        return None
    latest = sorted(files)[-1]
    LOG.info("Loading features from %s", latest)
    with fs.open(latest, "rb") as fh:
        df = pd.read_parquet(fh)
    return df

def upload_model_local(path, key):
    s3 = boto3.client("s3",
                      aws_access_key_id=s3cfg["access_key"],
                      aws_secret_access_key=s3cfg["secret_key"],
                      endpoint_url=s3cfg.get("endpoint_url"),
                      config=Config(signature_version="s3v4"))
    s3.upload_file(path, BUCKET, key)
    LOG.info("Uploaded model to %s/%s", BUCKET, key)

def main():
    df = download_latest_features()
    if df is None or df.empty:
        LOG.error("No features to train on.")
        return
    # simple feature selection: drop columns not numeric
    df = df.dropna(subset=['pm25_target_next24h'])
    y = df['pm25_target_next24h']
    X = df.drop(columns=['pm25_target_next24h','station_id','lat','lon','time'])
    # convert categ to numeric if any
    X = X.select_dtypes(include=['number']).fillna(-999)
    # time-based split
    tscv = TimeSeriesSplit(n_splits=3)
    # take last split as test
    train_idx, test_idx = list(tscv.split(X))[-1]
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    model = XGBRegressor(n_estimators=200, tree_method='hist', random_state=42)
    model.fit(X_train, y_train, eval_set=[(X_test,y_test)], early_stopping_rounds=20, verbose=True)
    os.makedirs("models", exist_ok=True)
    path = "models/xgb_v1.joblib"
    joblib.dump(model, path)
    upload_model_local(path, "models/xgb_v1.joblib")
    LOG.info("Training complete and model uploaded.")

if __name__ == "__main__":
    main()