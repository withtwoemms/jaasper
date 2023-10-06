import os

from botocore.exceptions import ClientError
from prefect_aws import AwsCredentials
from prefect_aws.s3 import S3Bucket

from jaasper import S3_BUCKET_BLOCK_NAME
from jaasper import S3_BUCKET_NAME
from jaasper import S3_BUCKET_PATH
from jaasper.blocks.storage.aws.credentials import AWS_CREDS_BUCKET_BLOCK_NAME



aws_credentials: AwsCredentials = AwsCredentials.load(AWS_CREDS_BUCKET_BLOCK_NAME)

s3_bucket = S3Bucket(
    bucket_name=S3_BUCKET_NAME,
    bucket_folder=S3_BUCKET_PATH,
    credentials=aws_credentials,
)

s3_client = aws_credentials.get_s3_client()
try:
    # check if the bucket exists
    response = s3_client.head_bucket(Bucket=S3_BUCKET_NAME)
except ClientError:
    s3_client.create_bucket(
        Bucket=S3_BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": aws_credentials.region_name}
    )

s3_bucket.save(S3_BUCKET_BLOCK_NAME, overwrite=True)
