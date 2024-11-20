import json

from dataclasses import asdict
from datetime import timedelta
from json import JSONEncoder

from flask.json.provider import JSONProvider

from jaaspr.models import Job, FakeResult


class SerializationPreProcessor(JSONEncoder):
    """Maps non-serializable types to serializable ones"""
    def default(self, obj):
        result = None
        match obj:
            case Job():
                result = asdict(obj)
            case timedelta():
                result = obj.total_seconds()  # Convert to seconds
            case Exception():
                result = repr(obj)
            case FakeResult():
                result = obj.value
            case _:
                result = super().default(obj)
        return result


class Serializer(JSONProvider):
    def dumps(self, obj: dict, **kwargs):
        return json.dumps(obj, cls=SerializationPreProcessor)
