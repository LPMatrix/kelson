from typing import Any, Dict, Callable
import importlib

class Container:
    """
    A simple Service Container for dependency injection.
    """
    _instances: Dict[str, Any] = {}
    _bindings: Dict[str, Callable[[], Any]] = {}

    @classmethod
    def bind(cls, key: str, resolver: Callable[[], Any]):
        """
        Register a binding with a resolver function.
        The resolver is called every time make() is called.
        """
        cls._bindings[key] = resolver

    @classmethod
    def singleton(cls, key: str, instance: Any):
        """
        Register a shared binding (singleton).
        """
        cls._instances[key] = instance

    @classmethod
    def make(cls, key: str) -> Any:
        """
        Resolve the given abstract type to the concrete instance.
        """
        if key in cls._instances:
            return cls._instances[key]
        
        if key in cls._bindings:
            return cls._bindings[key]()
            
        raise ValueError(f"Service '{key}' not found in container.")

    @classmethod
    def forget(cls, key: str):
        """
        Remove a binding from the container.
        """
        if key in cls._instances:
            del cls._instances[key]
        if key in cls._bindings:
            del cls._bindings[key]

def resolve(class_path: str) -> Any:
    """
    Helper to instantiate a class from a dot-notation string.
    e.g. 'app.Pipelines.LocalDataLoader'
    """
    try:
        module_name, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        cls_obj = getattr(module, class_name)
        return cls_obj()
    except (ValueError, ImportError, AttributeError) as e:
        raise ImportError(f"Could not resolve class '{class_path}': {e}")
