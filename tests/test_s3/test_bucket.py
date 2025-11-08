import pytest

@pytest.mark.default
def test_create_bucket(bucket, s3_client):
    existing_buckets = s3_client.list_buckets()["Buckets"]
    existing_buckets_names = [bucket["Name"] for bucket in existing_buckets]
    assert bucket in existing_buckets_names, f"Bucket {bucket} was not created."

@pytest.mark.extra
@pytest.mark.parametrize(
    's3_client, expected_region',
    [
    ("eu-central-1", "eu-central-1"),
    ("us-east-1", "us-east-1")
    ],
    indirect=["s3_client"])
def test_create_bucket_custom_region(bucket, s3_client, expected_region):
    existing_buckets = s3_client.list_buckets()["Buckets"]
    existing_buckets_names = [bucket["Name"] for bucket in existing_buckets]
    assert bucket in existing_buckets_names, f"Bucket {bucket} was not created."

    assert s3_client.meta.region_name == expected_region,\
        f"Client region is not {expected_region}. It is {s3_client.meta.region_name}."

    bucket_location = s3_client.get_bucket_location(Bucket=bucket)["LocationConstraint"]
    if expected_region == "us-east-1" and bucket_location is None:
        bucket_location = "us-east-1"
    assert bucket_location==expected_region, f'Bucket location is not {expected_region}. It is {bucket_location}.'