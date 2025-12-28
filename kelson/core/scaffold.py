import os
from pathlib import Path
from rich.console import Console
from rich.tree import Tree

class ProjectScaffolder:
    """
    Handles the creation of a new Kelson project structure.
    """
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.base_path = Path.cwd() / project_name
        self.console = Console()

    def build(self):
        """
        Builds the project directory structure and files.
        """
        if self.base_path.exists():
            self.console.print(f"[bold red]Error:[/bold red] Directory {self.project_name} already exists.")
            return

        self.create_directories()
        self.create_files()
        self.show_structure()

    def create_directories(self):
        """
        Creates the standard directory layout.
        """
        directories = [
            "app/Models",
            "app/Pipelines",
            "config",
            "database/datasets",
            "storage/checkpoints",
        ]

        for directory in directories:
            path = self.base_path / directory
            path.mkdir(parents=True, exist_ok=True)
            # Create __init__.py for python packages
            if directory.startswith("app"):
                (path / "__init__.py").touch()
        
        # Ensure app root package exists
        (self.base_path / "app" / "__init__.py").touch()

    def create_files(self):
        """
        Generates initial configuration and boilerplate files.
        """
        self._create_pyproject_toml()
        self._create_readme()
        self._create_config_file()
        self._create_base_model()

    @property
    def project_name_normalized(self):
        return self.project_name.replace("-", "_")

    def _create_pyproject_toml(self):
        toml_str = f"""[project]
name = "{self.project_name}"
version = "0.1.0"
description = "A Kelson ML Project"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "kelson",
    "typer",
    "rich",
    "pydantic",
    "pandas",
    "numpy",
]

[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]
"""
        with open(self.base_path / "pyproject.toml", "w") as f:
            f.write(toml_str)

    def _create_readme(self):
        content = f"""# {self.project_name}

Powered by [Kelson](https://github.com/kelson-ml/kelson) - A highly opinionated Machine Learning framework.
"""
        with open(self.base_path / "README.md", "w") as f:
            f.write(content)

    def _create_config_file(self):
        # Create a default config.yaml
        config_path = self.base_path / "config" / "app.yaml"
        content = """app:
  name: "My ML App"
  env: "local"
  debug: true

data:
  default_loader: "local"
  
storage:
  checkpoints_path: "storage/checkpoints"
"""
        with open(config_path, "w") as f:
            f.write(content)

    def _create_base_model(self):
        # We also need to ensure the user has the BaseModel definition available. 
        # Since Kelson is a framework, the BaseModel should be IN Kelson, and the user imports it.
        # But for now, we just set up the structure.
        pass

    def show_structure(self):
        tree = Tree(f"[bold blue]{self.project_name}/[/bold blue]")
        
        tree.add("app/")
        tree.add("config/")
        tree.add("database/")
        tree.add("storage/")
        tree.add("pyproject.toml")
        tree.add("README.md")
        
        self.console.print(tree)
