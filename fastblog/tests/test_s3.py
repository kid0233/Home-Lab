import os
import boto3
import pytest
from pathlib import Path
from io import BytesIO
from moto import mock_aws
from httpx import AsyncClient
from .conftest import create_test_user, login_user, auth_header


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["S3_BUCKET_NAME"] = "test-bucket"

"""
@pytest.fixture(scope="function")
def s3_client(aws_credentials):
    with mock_aws():
        yield boto3.client("s3", region_name="us-east-1")
"""



@pytest.fixture
def mocked_aws():
    with mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=os.environ["S3_BUCKET_NAME"])
        yield s3


def upload_file_to_s3(bucket_name, file_key, content):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=content)
    return True

def read_file_from_s3(bucket_name, file_key):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    return response["Body"].read().decode("utf-8")


def test_s3_upload_and_read(mocked_aws):
    bucket = "my-test-bucket"
    key = "hello.txt"
    data = "Hello World from Moto"

    mocked_aws.create_bucket(Bucket=bucket)

    success = upload_file_to_s3(bucket, key, data)
    assert success is True

    retrieved_content = read_file_from_s3(bucket, key)
    assert retrieved_content == data

