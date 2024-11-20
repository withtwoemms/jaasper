from celery import Celery

from jaaspr.config.worker import TaskEnvironment
from jaaspr.tasks import do_work


celery_task_manager = Celery(
    main='jaaspr.tasks',  # source from environment
    broker=TaskEnvironment.CELERY_BROKER_URL.value,
    backend=TaskEnvironment.CELERY_RESULT_BACKEND.value,
)

# -- TASK DECLARATIONS -----------------------------------------
do_work_function = celery_task_manager.task(do_work.function)
# --------------------------------------------------------------
