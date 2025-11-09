import pytest


@pytest.mark.default
def test_create_bucket(bucket: str, s3_client):
    """
    Test creating a bucket and verify its existence.
    :param bucket: created bucket name
    :param s3_client: S3 client
    """
    existing_buckets = s3_client.list_buckets()
    assert existing_buckets["ResponseMetadata"]["HTTPStatusCode"] == 200, "Failed to list buckets."
    existing_buckets_names = [bucket["Name"] for bucket in existing_buckets["Buckets"]]
    assert bucket in existing_buckets_names, f"Bucket {bucket} was not created."

@pytest.mark.default
def test_two_buckets_with_same_name(bucket: str, s3_client):
    """
    Test creating a bucket with a name that already exists and is owned by you.
    This should raise a BucketAlreadyOwnedByYou exception.
    :param bucket: Name of the existing bucket
    :param s3_client: S3 client
    """
    region = "eu-central-1"
    with pytest.raises(s3_client.exceptions.BucketAlreadyOwnedByYou) as err:
        s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region})
    assert "BucketAlreadyOwnedByYou" == err.value.response["Error"]["Code"]
    assert err.value.response["ResponseMetadata"]["HTTPStatusCode"] == 409, \
        f'HTTP status code is not 409. It is {err.value.response["ResponseMetadata"]["HTTPStatusCode"]}.'

@pytest.mark.extra
@pytest.mark.parametrize(
    's3_client, expected_region',
    [
    ("eu-central-1", "eu-central-1"),
    ("us-east-1", "us-east-1")
    ],
    indirect=["s3_client"])
def test_create_bucket_custom_region(bucket: str, s3_client, expected_region: str):
    """
    Test creating a bucket in provided region and verify its location.
    Test is parametrized to run for multiple regions.
    :param bucket: Bucket name
    :param s3_client: S3 client
    :param expected_region: S3 region where the bucket is created
    """
    existing_buckets = s3_client.list_buckets()
    assert existing_buckets["ResponseMetadata"]["HTTPStatusCode"] == 200, "Failed to list buckets."
    existing_buckets_names = [bucket["Name"] for bucket in existing_buckets["Buckets"]]
    assert bucket in existing_buckets_names, f"Bucket {bucket} was not created."

    assert s3_client.meta.region_name == expected_region,\
        f"Client region is not {expected_region}. It is {s3_client.meta.region_name}."

    bucket_location_response = s3_client.get_bucket_location(Bucket=bucket)
    assert bucket_location_response["ResponseMetadata"]["HTTPStatusCode"] == 200, "Failed to get bucket location."
    bucket_location = bucket_location_response["LocationConstraint"]
    if expected_region == "us-east-1" and bucket_location is None:
        bucket_location = "us-east-1"
    assert bucket_location==expected_region, f'Bucket location is not {expected_region}. It is {bucket_location}.'
