import pytest
import boto3
import uuid


def gen_bucket_name(prefix: str = 's3-test-task'):
    return f"{prefix}--{uuid.uuid4().hex}"

@pytest.fixture(scope='session')
def s3_client(request):
    region = getattr(request, "param", "us-east-1")
    return boto3.client('s3', region_name=region)

@pytest.fixture
def bucket(s3_client):
    bucket_name = gen_bucket_name()
    region = s3_client.meta.region_name
    if region == "us-east-1":
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        s3_client.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration={"LocationConstraint": region})
    yield bucket_name

    listed = s3_client.list_objects_v2(Bucket=bucket_name)
    if "Contents" in listed:
        s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={"Objects": [{"Key": obj["Key"]} for obj in listed["Contents"]]}
        )
    s3_client.delete_bucket(Bucket=bucket_name)
