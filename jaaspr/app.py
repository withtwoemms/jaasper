from flask import Flask, jsonify, request
from flask.wrappers import Response

from jaaspr.config.api import ApiEnvironment
from jaaspr.core.enums import AuxiliaryJobStates
from jaaspr.models import Job, FakeResult
from jaaspr.serialization import Serializer
from jaaspr.tasks import do_work_function


app = Flask(__name__)

app.json = Serializer(app)
# TODO: consider this logging format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s' | JSON
app.logger.setLevel(ApiEnvironment.FLASK_LOG_LEVEL.value)


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
    return jsonify(Job(job_id=job.id, status=AuxiliaryJobStates.ENQUEUED.name)), 202  # ENQUEUED


@app.route('/jobs/<string:job_id>/status', methods=['GET'])
def get_job_status(job_id):
    """Retrieve the current state of a job."""
    # Get the job result using the job_id
    job_result = FakeResult(state='PENDING', value='Job is pending.')
    
    # Build the response based on job status
    return jsonify(
        Job(
            job_id=job_id,
            status=job_result.state,  # Job's current state (e.g. PENDING, STARTED, SUCCESS, FAILURE)
            result=job_result
        )
    )


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
