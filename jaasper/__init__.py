import os


AWS_CREDS_BUCKET_BLOCK_NAME = os.environ.get(
    'JAASPER_AWS_CREDS_BUCKET_BLOCK_NAME',
    'aws-credentials'
)

S3_BUCKET_NAME = os.environ.get('JAASPER_S3_BUCKET_NAME', 'jaasper')
S3_BUCKET_PATH = os.environ.get('JAASPER_S3_BUCKET_PATH', 'testing')
S3_BUCKET_BLOCK_NAME = os.environ.get('JAASPER_S3_BUCKET_BLOCK_NAME', 's3')
S3_ENDPOINT_URL = os.environ.get('JAASPER_S3_ENDPOINT_URL', 'http://127.0.0.1:4566')
