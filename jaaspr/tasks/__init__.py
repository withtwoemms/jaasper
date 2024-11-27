from celery import Celery

from jaaspr.config.worker import TaskEnvironment
from jaaspr.tasks import do_work
from jaaspr.tasks import do_work_periodically


# TODO: encapsulate for provision in dependency injection scheme
celery_task_manager = Celery(
    main='jaaspr.tasks',  # source from environment
    broker=TaskEnvironment.CELERY_BROKER_URL.value,
    backend=TaskEnvironment.CELERY_RESULT_BACKEND.value,
)

# -- TASK DECLARATIONS -----------------------------------------
do_work_function = celery_task_manager.task(do_work.function)
do_work_periodically_function = celery_task_manager.task(do_work_periodically.function)
# --------------------------------------------------------------

# -- SCHEDULE DECLARATIONS (commented to address in future ) ---
# # TODO: consider support for `celery.schedules.crontab``
# # TODO: devise means of contolling schedule via config/API
# do_work_periodically_schedule = celery_task_manager.on_after_configure.connect(
#     do_work_periodically.schedule(do_work_periodically_function)
# )
# --------------------------------------------------------------
