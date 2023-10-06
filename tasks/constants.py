import os
from pathlib import Path


PROJECT_NAME = 'jaasper'

PROJECTROOT = Path(__file__).parent.parent
BLOCKSROOT = PROJECTROOT / PROJECT_NAME / 'blocks'
FLOWSROOT = PROJECTROOT / PROJECT_NAME / 'flows'

STORAGE_BLOCKSROOT = BLOCKSROOT / 'storage'
DATA_BLOCKSROOT = BLOCKSROOT / 'data'

ENTRYPOINT_MODULE_NAME = 'main'
ENTRYPOINT_FUNCTION_NAME = 'run'

S3_BUCKET_PATH = os.environ.get('JAASPER_S3_BUCKET_PATH', 'testing')
EXTRA_PIP_PACKAGES = os.environ.get(
    'EXTRA_PIP_PACKAGES',
    'prefect-aws'
)
