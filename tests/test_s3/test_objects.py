import pytest

@pytest.mark.default
def test_object_content(s3_client, bucket):
    file = "hello_s3.txt"
    content = "Hello S3"
    metadata = {"author": "test-object-content", "purpose": "test-metadata"}
    s3_client.put_object(Bucket=bucket, Body=content, Key=file, Metadata=metadata)
    response = s3_client.get_object(Bucket=bucket, Key=file)
    file_content = response["Body"].read().decode()
    assert file_content == content

    head = s3_client.head_object(Bucket=bucket, Key=file)
    print(head["Metadata"])
    assert head["Metadata"] == metadata
