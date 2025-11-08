import pytest
import boto3
import uuid
from log import log


def gen_bucket_name(prefix: str = 's3-test-task'):
    return f"{prefix}--{uuid.uuid4().hex}"

@pytest.fixture(scope='session')
def s3_client(request):
    region = getattr(request, "param", "us-east-1")
    log.info(f'Setting up S3 client for region "{region}"')
    return boto3.client('s3', region_name=region)

@pytest.fixture
def bucket(s3_client):
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
