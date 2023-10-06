import os
import yaml
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BlockRef:
    type: str
    envvar: str
    path: Path

    def __repr__(self):
        return f'{self.type}/{os.environ[self.envvar]}'


@dataclass
class DeploymentRef:
    path: Path

    def __repr__(self):
        deployment = yaml.safe_load(self.path.open())
        return f'{deployment["flow_name"]}/{deployment["name"]}'
