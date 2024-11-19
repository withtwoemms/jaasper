import pytest
from datetime import timedelta
from flask.json.provider import JSONProvider
from unittest.mock import Mock
import json

from jaaspr.serialization import SerializationPreProcessor, Serializer
from jaaspr.models import Job, FakeResult


@pytest.fixture
def fake_job():
    return Job(job_id=1, status="PENDING")


@pytest.fixture
def fake_result():
    return FakeResult(state="SUCCEDED", value="fake_value")


@pytest.fixture
def serializer():
    return Serializer()


def test_serialization_job(fake_job):
    encoder = SerializationPreProcessor()
    result = encoder.default(fake_job)
    assert result == {"job_id": 1, "status": "PENDING", "result": None}, "Job serialization failed"


def test_serialization_timedelta():
    encoder = SerializationPreProcessor()
    delta = timedelta(days=1, seconds=3600)
    result = encoder.default(delta)
    assert result == 90000, "Timedelta serialization failed"


def test_serialization_exception():
    encoder = SerializationPreProcessor()
    ex = ValueError("An error occurred")
    result = encoder.default(ex)
    assert result == "ValueError('An error occurred')", "Exception serialization failed"


def test_serialization_fake_result(fake_result):
    encoder = SerializationPreProcessor()
    result = encoder.default(fake_result)
    assert result == "fake_value", "FakeResult serialization failed"


def test_serialization_unknown_type():
    encoder = SerializationPreProcessor()
    unknown_obj = object()
    with pytest.raises(TypeError):
        encoder.default(unknown_obj)


def test_serializer_dumps(fake_job, fake_result):
    serializer = Serializer(app=Mock())
    data = {
        "job": fake_job,
        "result": fake_result,
        "delta": timedelta(minutes=30),
        "error": ValueError("Test error"),
    }
    json_output = serializer.dumps(data)
    parsed_output = json.loads(json_output)

    assert parsed_output["job"] == {"job_id": 1, "status": "PENDING", "result": None}, "Job dump failed"
    assert parsed_output["result"] == "fake_value", "FakeResult dump failed"
    assert parsed_output["delta"] == 1800, "Timedelta dump failed"
    assert "ValueError('Test error')" in parsed_output["error"], "Exception dump failed"
