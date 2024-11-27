from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

def function():
    """A simple task that simulating a scheduled job."""
    logger.info('Running scheduled job...')
    return 'Scheduled Job completed'
