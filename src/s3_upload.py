import boto3
from pathlib import Path


BUCKET_NAME = "texas-oil-data-jonathan-2026"

BRONZE_FILE = Path(
    "data/bronze/county_production/county_production.parquet"
)

BRONZE_KEY = "bronze/county_production/county_production.parquet"

SILVER_FILE = Path(
    "data/silver/county_production/county_production.parquet"
)

SILVER_KEY = "silver/county_production/county_production.parquet"


def get_s3_client():
    """Create and return an Amazon S3 client."""
    return boto3.client("s3")


def upload_file_to_s3(
    local_file: Path,
    bucket_name: str,
    object_key: str,
) -> None:
    """Upload a local file to Amazon S3."""
    s3_client = get_s3_client()

    s3_client.upload_file(
        str(local_file),
        bucket_name,
        object_key,
    )


def main() -> None:
    upload_file_to_s3(
        SILVER_FILE,
        BUCKET_NAME,
        SILVER_KEY,
    )

    print(
        f"Uploaded {SILVER_FILE} to "
        f"s3://{BUCKET_NAME}/{SILVER_KEY}"
    )



if __name__ == "__main__":
    main()