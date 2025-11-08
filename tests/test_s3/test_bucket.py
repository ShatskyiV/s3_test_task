import pytest
import botocore
from boto3 import client

@pytest.mark.default
def test_create_bucket(bucket: str, s3_client: client):
    existing_buckets = s3_client.list_buckets()["Buckets"]
    existing_buckets_names = [bucket["Name"] for bucket in existing_buckets]
    assert bucket in existing_buckets_names, f"Bucket {bucket} was not created."

@pytest.mark.default
def test_two_buckets_with_same_name(bucket: str, s3_client: client):
    region = "eu-central-1"
    try:
        s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region})
    except s3_client.exceptions.BucketAlreadyOwnedByYou as err:
       assert "BucketAlreadyOwnedByYou" == err.response["Error"]["Code"]

@pytest.mark.extra
@pytest.mark.parametrize(
    's3_client, expected_region',
    [
    ("eu-central-1", "eu-central-1"),
    ("us-east-1", "us-east-1")
    ],
    indirect=["s3_client"])
def test_create_bucket_custom_region(bucket: str, s3_client: client, expected_region: str):
    existing_buckets = s3_client.list_buckets()["Buckets"]
    existing_buckets_names = [bucket["Name"] for bucket in existing_buckets]
    assert bucket in existing_buckets_names, f"Bucket {bucket} was not created."

    assert s3_client.meta.region_name == expected_region,\
        f"Client region is not {expected_region}. It is {s3_client.meta.region_name}."

    bucket_location = s3_client.get_bucket_location(Bucket=bucket)["LocationConstraint"]
    if expected_region == "us-east-1" and bucket_location is None:
        bucket_location = "us-east-1"
    assert bucket_location==expected_region, f'Bucket location is not {expected_region}. It is {bucket_location}.'
