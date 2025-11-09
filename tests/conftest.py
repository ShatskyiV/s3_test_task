import pytest
import boto3
import uuid

from log import log


def gen_bucket_name(prefix: str = 's3-test-task')->str:
    """
    Generate unique bucket name with given prefix and random UUID4 suffix.
    :param prefix: Bucket name prefix
    :return: Unique bucket name
    """
    return f"{prefix}--{uuid.uuid4().hex}"

@pytest.fixture(scope='session')
def s3_client(request: pytest.FixtureRequest):
    """
    Setup S3 client for the given region.
    This is a session-scoped fixture that provides a boto3 S3 client once per test session.
    The region can be specified via the 'request' parameter; if not provided, it defaults to 'us-east-1'.
    :param request: Parameter to specify the AWS region for the S3 client
    :return: Boto3 S3 client
    """
    region = getattr(request, "param", "us-east-1")
    log.info(f'Setting up S3 client for region "{region}"')
    return boto3.client('s3', region_name=region)

@pytest.fixture
def bucket(s3_client):
    """
    This fixture creates a new S3 bucket before a test and deletes it after the test,
    deleting all objects within it first.
    It yields the name of the created bucket to the test.
    :param s3_client: S3 client fixture
    """
    bucket_name = gen_bucket_name()
    region = s3_client.meta.region_name
    log.info("Creating new bucket.")
    if region == "us-east-1":
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        s3_client.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration={"LocationConstraint": region})
    log.info(f'New bucket with name "{bucket_name}" is created for region "{region}"')
    yield bucket_name
    log.info(f'Deleting all object in bucket "{bucket_name}" and bucket itself.')
    listed = s3_client.list_objects_v2(Bucket=bucket_name)
    if "Contents" in listed:
        s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={"Objects": [{"Key": obj["Key"]} for obj in listed["Contents"]]}
        )
    s3_client.delete_bucket(Bucket=bucket_name)
