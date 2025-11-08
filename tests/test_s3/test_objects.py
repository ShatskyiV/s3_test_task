import pytest


@pytest.mark.default
def test_object_content(s3_client, bucket):
    key = "hello_s3.txt"
    content = "Hello S3"
    metadata = {"author": "test-object-content", "purpose": "test-metadata"}
    s3_client.put_object(Bucket=bucket, Body=content, Key=key, Metadata=metadata)
    response = s3_client.get_object(Bucket=bucket, Key=key)
    file_content = response["Body"].read().decode()
    assert file_content == content

    head = s3_client.head_object(Bucket=bucket, Key=key)
    assert head["Metadata"] == metadata

@pytest.mark.default
def test_get_nonexistent_object(s3_client, bucket):
    file = "hello_s3.txt"
    try:
        s3_client.get_object(Bucket=bucket, Key=file)
    except s3_client.exceptions.NoSuchKey as err:
        assert "NoSuchKey" == err.response["Error"]["Code"], f'Error "NoSuchKey" is not present in response.'

@pytest.mark.default
def test_objects_listing(s3_client, bucket):
    prefix = "s3-listing-test"
    uploaded = list()
    for num in range(15):
        key = f"{prefix}-{num}"
        content = f"This is file object number {num}"
        s3_client.put_object(Bucket=bucket, Body=content, Key=key)
        uploaded.append(key)
    listed = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    keys = [obj["Key"] for obj in listed["Contents"]]
    for key in uploaded:
        assert key in keys, f'File object "{key}" is not present in listed objects.'

@pytest.mark.extra
def test_download_by_presigned_url(s3_client, bucket):
    import requests
    key = "presigned_ulr.txt"
    content = "Hello S3"
    s3_client.put_object(Bucket=bucket, Body=content, Key=key)
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=60,
    )
    assert url is not None, "URL was not generated."
    response = requests.get(url)
    assert response.status_code == 200
    assert response.content.decode() == content