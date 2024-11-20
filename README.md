# jaaspr
the Jobs as a Service, Provisioned Runtime

# Usage

Export all subproject dependencies:
```
poetry run export-api-deps
```
Given a `.env` file akin to the following at PROJECTROOT:
```
REDIS_DB_NUM=0
REDIS_PORT=6379
REDIS_HOST=redis
CELERY_APP=jaaspr.tasks
CELERY_BROKER_URL=${REDIS_HOST}://${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB_NUM}
CELERY_RESULT_BACKEND=${REDIS_HOST}://${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB_NUM}
CELERY_LOG_LEVEL=INFO
CELERY_MONITORING_PORT=5555
FLASK_APP=jaaspr.app:app
FLASK_DEBUG=
FLASK_ENV=development
FLASK_LOG_LEVEL=DEBUG
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=1234
WSGI_SERVER=waitress
WSGI_SERVER_LOG_LEVEL=DEBUG
```
build and run the containers like so:
```
docker-compose up --build
```

# Development

### Setup

The project uses [`poetry`](https://github.com/python-poetry/poetry) as its buildtool.
All dependencies can be installed with:
```
poetry install
```
There are (uninstalled) `poetry` scripts that export individual "requirements.txt" files for dependency groups defined in the "pyproject.toml" file.
An example being as follows:
```
poetry run export-api-deps
```
