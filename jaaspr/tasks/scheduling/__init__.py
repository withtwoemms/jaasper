import threading
from collections import defaultdict
from celery import Celery


# Registry to track tasks using defaultdict (task_name |-> timer)
task_registry = defaultdict(dict)  # TODO: persist registry to some backend
lock = threading.Lock()  # ensures thread safety when modifying the registry


def custom_scheduler(celery_app: Celery, task_name: str, interval: int, args=None):
    """
    Schedule a Celery task dynamically with replacement of existing tasks.

    :param celery_app: Owner of the task to be scheduled.
    :param task_name: Unique name for the task.
    :param interval: Interval in seconds for repeated execution.
    :param args: Arguments to pass to the task.
    
    TODO: give further considerations to means of doing this via the `celery` standard lib
    TODO: inject logger; replace `print` statements
    """
    if args is None:
        args = []

    def run_task():
        celery_app.send_task(task_name, args=args)

        # Schedule the next execution
        with lock:
            task_registry[task_name]['timer'] = threading.Timer(interval, run_task)
            task_registry[task_name]['timer'].start()

    with lock:
        # Replace the task if it already exists
        if task_name in task_registry:
            print(f"Replacing existing task: {task_name}")
            task_registry[task_name]['timer'].cancel()  # Stop the current timer

        # Schedule the new task
        print(f"Scheduling task: {task_name} every {interval} seconds.")
        task_registry[task_name] = {'interval': interval, 'args': args}
        task_registry[task_name]['timer'] = threading.Timer(interval, run_task)
        task_registry[task_name]['timer'].start()
