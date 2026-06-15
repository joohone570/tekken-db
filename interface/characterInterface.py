from abc import ABC, abstractmethod
import pandas as pd

@abstractmethod
class Iprimary_skillInterface(ABC):
    def save(self, id) -> int:
        ...
    def find_all(self) -> pd.DataFrame:
        ...