from enum import Enum, auto
from os import environ
from typing import Optional


class FromEnviron(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        envvar = environ.get(name)
        if envvar is None:
            raise ValueError(f'Environment variable declared, but undefined: {name}')
        return envvar

    def coerce_value(self, type: Optional[type] = None):
        if type is not None:
            return type(self._value_)
        return self._value_


class ValueMatchesName(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name


# TODO: consider formalizing auxiliary state integration
class AuxiliaryJobStates(ValueMatchesName):
    CANCELLED = auto()
    ENQUEUED = auto()