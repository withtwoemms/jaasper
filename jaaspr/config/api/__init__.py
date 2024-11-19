from enum import auto

from jaaspr.core.enums import FromEnviron


# TODO: generat secret key for API access (e.g. app.config.update(SECRET_KEY=???))
class ApiEnvironment(FromEnviron):
    CELERY_BROKER_URL = auto()
    CELERY_RESULT_BACKEND = auto()
    FLASK_LOG_LEVEL = auto()
    FLASK_DEBUG = auto()
    FLASK_ENV = auto()
    FLASK_APP = auto()
    FLASK_RUN_HOST = auto()
    FLASK_RUN_PORT = auto()
    REDIS_HOST = auto()
    REDIS_PORT = auto()
    REDIS_DB_NUM = auto()
