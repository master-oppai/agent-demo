from abc import ABC, abstractmethod
from pydantic import BaseModel
import pandas as pd

class NIDSSource:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        # normalize for lookups
        self.df.columns = [c.strip() for c in self.df.columns]
        self.df['Support Item Number'] = self.df['Support Item Number'].astype(str).str.strip()

    def validate_item(self, item_code: str):
        """Check if an item code exists in the NIDS source."""
        return item_code in self.df['Support Item Number'].values

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
