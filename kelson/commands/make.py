import typer
from rich.console import Console
from pathlib import Path
import re

console = Console()

def to_snake_case(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def make_model(name: str = typer.Argument(..., help="The name of the model class")):
    """
    Scaffold a new model class.
    """
    # Check if we are in a kelson project (simple check)
    if not Path("app/Models").exists():
        console.print("[bold red]Error:[/bold red] app/Models directory not found. Are you in a Kelson project?")
        raise typer.Exit(code=1)

    snake_name = to_snake_case(name)
    file_path = Path(f"app/Models/{snake_name}.py")

    if file_path.exists():
        console.print(f"[bold red]Error:[/bold red] Model {name} already exists at {file_path}.")
        raise typer.Exit(code=1)

    template = f"""from kelson.core.model import BaseModel
from typing import Any

class {name}(BaseModel):
    \"\"\"
    {name} model definition.
    \"\"\"
    # Define hyperparameters as Pydantic fields
    learning_rate: float = 0.001
    batch_size: int = 32

    def load_data(self) -> Any:
        \"\"\"
        Load data for the model.
        \"\"\"
        # TODO: Implement data loading
        pass

    def transform(self, data: Any) -> Any:
        \"\"\"
        Preprocess the data.
        \"\"\"
        # TODO: Implement data transformation
        return data

    def build(self) -> Any:
        \"\"\"
        Build the model architecture.
        \"\"\"
        # TODO: Return your model (e.g. sklearn, torch, tensorflow)
        pass

    def fit(self, data: Any) -> Any:
        \"\"\"
        Train the model.
        \"\"\"
        # TODO: Implement training loop
        pass
"""
    
    with open(file_path, "w") as f:
        f.write(template)

    console.print(f"[bold green]Success![/bold green] Model [bold white]{name}[/bold white] created at [underline]{file_path}[/underline].")
