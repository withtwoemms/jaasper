from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar('T')

@dataclass
class Job(Generic[T]):
    job_id: str
    status: str
    result: Optional[T] = None
