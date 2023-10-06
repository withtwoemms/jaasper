from prefect_aws import AwsCredentials, AwsClientParameters

from jaasper import AWS_CREDS_BUCKET_BLOCK_NAME
from jaasper import S3_ENDPOINT_URL


aws_client_params = AwsClientParameters(
    verify=False,  # TODO -- source from env
    endpoint_url=S3_ENDPOINT_URL
)

AwsCredentials(
    aws_access_key_id='no-access-key-id',  # TODO -- source from env
    aws_secret_access_key='no-secret-access-key',  # TODO -- source from env
    aws_session_token='no-session-token',  # TODO -- source from env
    region_name="us-east-2",
    aws_client_parameters=aws_client_params,
).save(AWS_CREDS_BUCKET_BLOCK_NAME, overwrite=True)
