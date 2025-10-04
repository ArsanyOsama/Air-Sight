import boto3, json, os

def get_s3():
    # Always resolve path relative to project root
    base_dir = os.path.dirname(os.path.dirname(__file__))  # go up from scripts/
    config_path = os.path.join(base_dir, "config.json")

    with open(config_path) as f:
        config = json.load(f)

    key_id = config["cloud"]["key_id"]
    app_key = config["cloud"]["application_key"]
    endpoint = f"https://{config['cloud']['endpoint']}"
    bucket = config["cloud"]["bucket"]

    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=key_id,
        aws_secret_access_key=app_key
    )
    return s3, bucket
