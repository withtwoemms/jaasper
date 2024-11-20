from enum import Enum, auto


class SubProjects(Enum):
    API = auto()
    WORKER = auto()

    @property
    def name(self):
        return self._name_.lower()
