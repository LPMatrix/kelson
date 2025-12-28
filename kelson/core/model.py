from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel as PydanticBaseModel, ConfigDict, PrivateAttr

class BaseModel(PydanticBaseModel, ABC):
    """
    The abstract base class for all Kelson models.
    Uses Pydantic for validation and configuration management.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    _tracker: Any = PrivateAttr(default=None)

    def set_tracker(self, tracker: Any):
        """
        Internal use: attach a progress tracker.
        """
        self._tracker = tracker

    def log(self, metrics: Dict[str, Any]):
        """
        Log training metrics (e.g., {'epoch': 1, 'loss': 0.5, 'accuracy': 0.9}).
        """
        if self._tracker:
            self._tracker.update(metrics)

    @abstractmethod
    def load_data(self) -> Any:
        """
        Load raw data from source.
        """
        pass

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """
        Preprocess and transform the raw data into model-ready format.
        """
        pass

    @abstractmethod
    def build(self) -> Any:
        """
        Build and return the underlying model architecture.
        """
        pass

    @abstractmethod
    def fit(self, data: Any) -> Any:
        """
        Train the model on the provided data.
        """
        pass
