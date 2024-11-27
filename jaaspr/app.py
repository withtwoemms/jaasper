from celery.result import AsyncResult
from flask import Flask, jsonify, request
from flask.wrappers import Response
from redis import StrictRedis

from jaaspr.config.api import ApiEnvironment
from jaaspr.core.enums import AuxiliaryJobStates
from jaaspr.models import Job
from jaaspr.serialization import Serializer
from jaaspr.tasks import do_work_function
from jaaspr.tasks import celery_task_manager
from jaaspr.tasks.scheduling import custom_scheduler


app = Flask(__name__)

app.json = Serializer(app)
# TODO: consider this logging format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s' | JSON
app.logger.setLevel(ApiEnvironment.FLASK_LOG_LEVEL.value)

redis = StrictRedis(
    host=ApiEnvironment.REDIS_HOST.value,
    port=ApiEnvironment.REDIS_PORT.value,
    db=ApiEnvironment.REDIS_DB_NUM.value,
    decode_responses=True
)


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method Not Allowed'}), 405

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': f'Unsupported route: "{request.path}"'}), 404


# API Endpoints

# TODO: should not be publically accessible
@app.route("/config", methods=['GET'])
def config():
    return jsonify(app.config.copy())


# TODO: add means of selecting job
@app.route("/jobs", methods=['POST'])
def create_job():
    """Create a new job with an initial state of RECEIVED."""
    job = do_work_function.apply_async()
    redis.sadd("all_jobs", job.id)  # TODO: source set name from environment
    return jsonify(Job(job_id=job.id, status=AuxiliaryJobStates.ENQUEUED.name)), 202  # ENQUEUED


@app.route("/jobs/schedule", methods=['POST'])
def schedule_job():
    """Dynamically schedule a Job."""
    data = request.get_json(silent=True)

    # TODO: formalize this validation by use of some model
    if not data or 'seconds' not in data or 'name' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    # TODO: capture and persist result of scheduled task execution
    custom_scheduler(celery_task_manager, data['name'], data['seconds'], None)

    return jsonify({"status": "Periodic task scheduled", "interval": data['seconds']}), 201


@app.route('/jobs', methods=['GET'])
def get_all_jobs():
    # Optional query parameter to filter by state
    state_filter = request.args.get('state')

    # Retrieve all job IDs from Redis
    job_ids = redis.smembers("all_jobs")

    jobs = []
    for job_id in job_ids:
        job_result = AsyncResult(job_id, app=celery_task_manager)

        # Include only jobs that match the requested state (if provided)
        if state_filter is None or job_result.state == state_filter.upper():
            jobs.append(
                Job(
                    job_id=job_id,
                    status=job_result.state,
                    result=job_result
                )
            )

    return jsonify(jobs)


@app.route('/jobs/<string:job_id>/status', methods=['GET'])
def get_job_status(job_id):
    """Retrieve the current state of a job."""
    # Get the job result using the job_id
    job_result = AsyncResult(job_id, app=celery_task_manager)

    # Build the response based on job status
    return jsonify(
        Job(
            job_id=job_id,
            status=job_result.state,  # Job's current state (e.g. PENDING, STARTED, SUCCESS, FAILURE)
            result=job_result
        )
    )


@app.route('/jobs/<string:job_id>/cancel', methods=['POST'])
def cancel_job(job_id):
    # Retrieve the job
    job = AsyncResult(job_id, app=celery_task_manager)

    # Check if the job is still pending or active
    if job.state in ['PENDING', 'RECEIVED', 'STARTED']:
        # Revoke the job (terminate if active)
        job.revoke(terminate=True)
        return jsonify(Job(job_id=job_id, status=AuxiliaryJobStates.CANCELLED.name))  # CANCELLED
    else:
        # If the job is already finished, we cannot cancel it
        return {'error': f'Job is already {job.state} and cannot be cancelled'}, 400


@app.after_request
def log_requests(resp: Response):
    app.logger.info(f'{request.method} {request.path} | {resp.status_code}')
    return resp


# Run the app
if __name__ == '__main__':
    app.run(
        host=ApiEnvironment.FLASK_RUN_HOST.value,
        port=ApiEnvironment.FLASK_RUN_PORT.value,
        debug=ApiEnvironment.FLASK_DEBUG.coerce_value(type=bool),
    )
