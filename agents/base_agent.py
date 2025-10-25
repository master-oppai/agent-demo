from abc import ABC, abstractmethod
from pydantic import BaseModel


class ProcessResponse(BaseModel):
    is_valid: bool
    reason: str


class BaseAgent(ABC):
    @abstractmethod
    def __init__(self, model: str):
        pass

    @abstractmethod
    def process(self, data: str) -> ProcessResponse:
        pass
