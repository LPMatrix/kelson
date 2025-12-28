from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel as PydanticBaseModel, ConfigDict

class BaseModel(PydanticBaseModel, ABC):
    """
    The abstract base class for all Kelson models.
    Uses Pydantic for validation and configuration management.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

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
