from prefect import flow, task
from prefect.logging import get_logger


logger = get_logger(__name__)


@task
def say(message: str):
    logger.info(message)


@flow(name='hello')
def run(message='sup!'):
    say(message)
