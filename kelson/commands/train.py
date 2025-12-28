import typer
import importlib
import sys
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from kelson.commands.make import to_snake_case
# We import BaseModel just for type hinting if needed, but we don't strictly need it at runtime if using duck typing or runtime checks.
# But good to have.
from kelson.core.model import BaseModel

console = Console()

def train_model(model_name: str = typer.Argument(..., help="The name of the model to train")):
    """
    Train a specified model.
    """
    # Ensure CWD is in sys.path
    if os.getcwd() not in sys.path:
        sys.path.append(os.getcwd())

    snake_name = to_snake_case(model_name)
    module_path = f"app.Models.{snake_name}"
    
    try:
        module = importlib.import_module(module_path)
        model_class = getattr(module, model_name)
    except (ImportError, AttributeError) as e:
        console.print(f"[bold red]Error:[/bold red] Model [bold white]{model_name}[/bold white] not found.")
        console.print(f"Expected file: app/Models/{snake_name}.py")
        console.print(f"Expected class: {model_name}")
        console.print(f"Details: {e}")
        raise typer.Exit(code=1)

    # Instantiate model
    try:
        # TODO: Load hyperparameters from config/app.yaml or config/models.yaml and pass them?
        # For now, we rely on default values defined in the class or Pydantic validation.
        model = model_class()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to instantiate {model_name}: {e}")
        raise typer.Exit(code=1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        
        # 1. Load Data
        task1 = progress.add_task(description="Loading data...", total=None)
        try:
            data = model.load_data()
            progress.update(task1, completed=1, description="[green]Data loaded[/green]")
        except Exception as e:
            console.print(f"[bold red]Error during load_data:[/bold red] {e}")
            raise typer.Exit(code=1)

        # 2. Transform
        task2 = progress.add_task(description="Transforming data...", total=None)
        try:
            data = model.transform(data)
            progress.update(task2, completed=1, description="[green]Data transformed[/green]")
        except Exception as e:
            console.print(f"[bold red]Error during transform:[/bold red] {e}")
            raise typer.Exit(code=1)

        # 3. Build
        task3 = progress.add_task(description="Building model architecture...", total=None)
        try:
            model.build()
            progress.update(task3, completed=1, description="[green]Model built[/green]")
        except Exception as e:
            console.print(f"[bold red]Error during build:[/bold red] {e}")
            raise typer.Exit(code=1)

        # 4. Fit
        task4 = progress.add_task(description="Training model...", total=None)
        try:
            model.fit(data)
            progress.update(task4, completed=1, description="[green]Model trained[/green]")
        except Exception as e:
            console.print(f"[bold red]Error during fit:[/bold red] {e}")
            raise typer.Exit(code=1)

    console.print(f"\n[bold green]Training completed successfully for {model_name}![/bold green]")
