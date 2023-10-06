from typing import Optional

from invoke import task
from invoke.context import Context

from tasks.constants import ENTRYPOINT_MODULE_NAME
from tasks.constants import S3_BUCKET_PATH
from tasks.enums import Blocks
from tasks.enums import Flows
from tasks.enums import StorageBlocks
from tasks.execution import run_command
from tasks.types import BlockRef


@task(optional=['dry-run'])
def register_block(
    ctx: Context,
    type: str,
    name: str,
    dry_run: Optional[str] = False,
):
    """Regsiters a block of given [name] and [type].
    """
    blockref: BlockRef = Blocks[type].subtype[name].value
    cmd = f'prefect block register --file {blockref.path}'
    if dry_run:
        cmd = f'echo {cmd}'
    return run_command(cmd)


@task(optional=['dry-run'])
def build_deployment(
    ctx: Context,
    flow: str,
    sblock: str,
    work_pool: str,                                                                           
    apply: Optional[str] = False,
    dry_run: Optional[str] = False,
):
    flow: Flows = Flows[flow]
    sblock: StorageBlocks = StorageBlocks[sblock]
    cmd = (
        f'prefect deployment build {flow.entrypoint} '
        f'--name {ENTRYPOINT_MODULE_NAME} '
        '--infra docker-container '  # should be paraeterizable
        f'--storage-block {sblock.ref} '
        f'--pool {work_pool} '
        f'--output {flow.deployment.path} '
        f'--path {S3_BUCKET_PATH} '
        f'--override env.EXTRA_PIP_PACKAGES=prefect-aws '  # optional; should be paraeterizable
    )
    if apply:
        cmd += '--apply'
    if dry_run:
        cmd = f'echo {cmd}'
    return run_command(cmd)


@task(optional=['dry-run'])
def run_deployment(
    ctx: Context,
    flow: str,
    dry_run: Optional[str] = False,
):
    """Runs a given deloyment.
    """
    cmd = f'prefect deployment run {Flows[flow].ref}'
    if dry_run:
        cmd = f'echo {cmd}'
    return run_command(cmd)


@task(optional=['dry-run'])
def create_pool(ctx: Context, name: str, type: str, dry_run: Optional[str] = False,):
    """Creates prefect work pool.
    """
    cmd = f'prefect work-pool create {name} --type {type}'
    if dry_run:
        cmd = f'echo {cmd}'
    run_command(cmd)


@task(optional=['dry-run'])
def run_agent(ctx: Context, work_pool: str, dry_run: Optional[str] = False,):
    """Runs prefect agent.
    """
    cmd = f'prefect agent start --pool {work_pool}'
    if dry_run:
        cmd = f'echo {cmd}'
    run_command(cmd)


@task(optional=['dry-run'])
def run_prefect_server(ctx: Context, dry_run: Optional[str] = False,):
    """Runs prefect server.
    """
    cmd = f'prefect server start'
    if dry_run:
        cmd = f'echo {cmd}'
    run_command(cmd)


@task(optional=['dry-run'])
def run_localstack(ctx: Context, dry_run: Optional[str] = False,):
    """Runs localstack container.
    """
    cmd = (
        'docker run --rm -it '
        '-p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack'
    )
    if dry_run:
        cmd = f'echo {cmd}'
    run_command(cmd)


@task(optional=['dry-run'])
def run_postgres(ctx: Context, dry_run: Optional[str] = False,):
    """Runs postgres container.
    """
    # cmd = 'docker compose up'
    cmd = 'docker run -it --name prefect-postgres -v prefectdb:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_USER=jaasper -e POSTGRES_PASSWORD=jaasper -e POSTGRES_DB=jaasper postgres:latest'
    if dry_run:
        cmd = f'echo {cmd}'
    run_command(cmd)


def init(ctx: Context, dry_run: Optional[str] = False,):
    """Initializes the runtime:

    * start/provision job server database (local)
    * create work pool(s)
    * start jobs server (local)
    * start agent
    * build deployment(s)
    """
    raise NotImplementedError


def reset(ctx: Context, dry_run: Optional[str] = False,):
    raise NotImplementedError
