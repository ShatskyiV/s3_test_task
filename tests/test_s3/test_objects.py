import pytest


@pytest.mark.default
def test_object_content(s3_client, bucket):
    """
    Tests uploading an object to S3, downloading it, and verifying if its content and metadata are same as expected.
    :param s3_client: S3 client
    :param bucket: Bucket name
    """
    key = "hello_s3.txt"
    content = "Hello S3"
    metadata = {"author": "test-object-content", "purpose": "test-metadata"}
    put_response = s3_client.put_object(Bucket=bucket, Body=content, Key=key, Metadata=metadata)
    assert put_response["ResponseMetadata"]["HTTPStatusCode"] == 200, "Failed to upload object to S3."
    get_response = s3_client.get_object(Bucket=bucket, Key=key)
    assert get_response["ResponseMetadata"]["HTTPStatusCode"] == 200, "Failed to download object from S3."
    file_content = get_response["Body"].read().decode()
    assert file_content == content

    head_response = s3_client.head_object(Bucket=bucket, Key=key)
    assert head_response["ResponseMetadata"]["HTTPStatusCode"] == 200, "Failed to retrieve head object from S3."
    assert head_response["Metadata"] == metadata

@pytest.mark.default
def test_get_nonexistent_object(s3_client, bucket):
    """
    Tests attempting to download a non-existent object from S3 and expects a NoSuchKey error.
    :param s3_client: S3 client
    :param bucket: Bucket name
    """
    file = "hello_s3.txt"
    with pytest.raises(s3_client.exceptions.NoSuchKey) as err:
        s3_client.get_object(Bucket=bucket, Key=file)
    assert "NoSuchKey" == err.value.response["Error"]["Code"], f'Error "NoSuchKey" is not present in response.'
    assert err.value.response["ResponseMetadata"]["HTTPStatusCode"] == 404, \
        f'HTTP status code is not 404 for non-existent object download.'

@pytest.mark.default
def test_objects_listing(s3_client, bucket):
    """
    Tests uploading multiple objects to S3 and listing them to verify their presence.
    :param s3_client: S3 client
    :param bucket: Bucket name
    """
    prefix = "s3-listing-test"
    uploaded = list()
    for num in range(15):
        key = f"{prefix}-{num}"
        content = f"This is file object number {num}"
        put_response = s3_client.put_object(Bucket=bucket, Body=content, Key=key)
        assert put_response["ResponseMetadata"]["HTTPStatusCode"] == 200, f'Failed to upload object "{key}" to S3.'
        uploaded.append(key)
    listed = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    assert listed["ResponseMetadata"]["HTTPStatusCode"] == 200, "Failed to list objects in S3."
    keys = [obj["Key"] for obj in listed["Contents"]]
    for key in uploaded:
        assert key in keys, f'File object "{key}" is not present in listed objects.'

@pytest.mark.extra
def test_download_by_presigned_url(s3_client, bucket):
    """
    Tests generating a presigned URL for an S3 object, downloading it using that URL and verifying its content.
    :param s3_client: S3 client
    :param bucket: Bucket name
    """
    import requests
    key = "presigned_ulr.txt"
    content = "Hello S3"
    put_response = s3_client.put_object(Bucket=bucket, Body=content, Key=key)
    assert put_response["ResponseMetadata"]["HTTPStatusCode"] == 200, "Failed to upload object to S3."
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=60,
    )
    assert url is not None, "URL was not generated."
    response = requests.get(url)
    assert response.status_code == 200
    assert response.content.decode() == content