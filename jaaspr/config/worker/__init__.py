from enum import auto

from jaaspr.core.enums import FromEnviron


class TaskEnvironment(FromEnviron):
    CELERY_BROKER_URL = auto()
    CELERY_RESULT_BACKEND = auto()
