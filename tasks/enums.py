from enum import Enum
from pathlib import Path

from tasks.constants import DATA_BLOCKSROOT
from tasks.constants import ENTRYPOINT_MODULE_NAME
from tasks.constants import ENTRYPOINT_FUNCTION_NAME
from tasks.constants import FLOWSROOT
from tasks.constants import STORAGE_BLOCKSROOT
from tasks.types import BlockRef
from tasks.types import DeploymentRef


class Flows(Enum):
    HELLO: Path = FLOWSROOT / 'hello'

    @property
    def ref(self):
        return str(self.deployment)
        # return self.value.stem.lower().replace('_', '-')

    @property
    def path(self) -> Path:
        return self.value

    @property
    def entrypoint(self) -> str:
        return f'{self.path / ENTRYPOINT_MODULE_NAME}.py:{ENTRYPOINT_FUNCTION_NAME}'

    @property
    def deployment(self):
        return DeploymentRef(
            path=self.path / f'{ENTRYPOINT_FUNCTION_NAME}_deployment.yaml'
        )
    
    def __getitem__(self, key) -> 'Flows':
        return Flows[key]


class Resources(Enum):

    @property
    def value(self) -> BlockRef:
        return super().value

    @property
    def path(self):
        return self.value.path

    @property
    def ref(self):
        return str(self.value)


class StorageBlocks(Resources):
    AWS_CREDS: BlockRef = BlockRef(
        type='aws-credentials',
        envvar='JAASPER_AWS_CREDS_BUCKET_BLOCK_NAME',
        path=STORAGE_BLOCKSROOT / 'aws' / 'credentials.py',
    )
    S3: BlockRef = BlockRef(
        type='s3-bucket',
        envvar='JAASPER_S3_BUCKET_BLOCK_NAME',
        path=STORAGE_BLOCKSROOT / 'aws' / 's3.py',
    )
    

class DataBlocks(Resources):
    DATETIME: BlockRef = BlockRef(
        type='datetime',
        envvar='JAASPER_DATETIME_BLOCK_NAME',
        path=DATA_BLOCKSROOT / 'datetime.py'
    )
    JSON: BlockRef = BlockRef(
        type='json',
        envvar='JAASPER_JSON_BLOCK_NAME',
        path=DATA_BLOCKSROOT / 'json.py',
    )


class Blocks(Enum):
    STORAGE: StorageBlocks = StorageBlocks
    DATA: DataBlocks = DataBlocks

    @property
    def subtype(self):
        return self.value
