import yaml
from pathlib import Path
from typing import Any, Dict

class Config:
    _config: Dict[str, Any] = {}

    @classmethod
    def load(cls, path: Path = Path("config")):
        """
        Load all YAML config files from the given directory.
        """
        if not path.exists():
            return
        
        for file in path.glob("*.yaml"):
            key = file.stem
            try:
                with open(file, "r") as f:
                    content = yaml.safe_load(f)
                    if content:
                        cls._config[key] = content
            except Exception as e:
                print(f"Error loading config {file}: {e}")

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get config value using dot notation: app.name
        """
        keys = key.split(".")
        value = cls._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
