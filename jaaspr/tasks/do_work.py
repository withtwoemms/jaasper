from time import sleep

from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

def function():
    """A simple task that simulates a job."""
    logger.info('Processing job...')
    sleep(30)  # Simulate some time-consuming task
    return 'Job completed'
