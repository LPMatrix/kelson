import typer
import importlib
import sys
import os
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from kelson.commands.make import to_snake_case
# We import BaseModel just for type hinting if needed, but we don't strictly need it at runtime if using duck typing or runtime checks.
# But good to have.
from kelson.core.model import BaseModel
from kelson.core.config import Config
from typing import Dict, Any, List

console = Console()

class TrainingDashboard:
    """
    Manages the Rich Live display for training progress.
    """
    def __init__(self, model_name: str, config: Dict[str, Any]):
        self.model_name = model_name
        self.config = config
        self.metrics_history: List[Dict[str, Any]] = []
        
        # Components
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
        )
        self.task_id = self.progress.add_task(f"Training {model_name}...", total=None)
        
        self.table = Table(title="Training Metrics", expand=True)
        self.table.add_column("Epoch", justify="right", style="cyan", no_wrap=True)
        self.table.add_column("Loss", justify="right", style="magenta")
        self.table.add_column("Accuracy", justify="right", style="green")
        # Dynamic columns can be added later if we want generic metrics
        
        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="body"),
        )
        self.layout["header"].update(
            Panel(f"Training [bold white]{model_name}[/bold white] with config: {config}", style="blue")
        )
        self.layout["body"].split_row(
            Layout(name="progress", ratio=1),
            Layout(name="metrics", ratio=2),
        )
        self.layout["progress"].update(Panel(self.progress, title="Status"))
        self.layout["metrics"].update(Panel(self.table, title="History"))

    def update(self, metrics: Dict[str, Any]):
        """
        Update the dashboard with new metrics.
        Expected keys: 'epoch', 'loss', 'accuracy' (optional)
        """
        self.metrics_history.append(metrics)
        
        epoch = metrics.get("epoch", len(self.metrics_history))
        loss = metrics.get("loss", "N/A")
        acc = metrics.get("accuracy", metrics.get("acc", "N/A"))
        
        # Format values
        f_loss = f"{loss:.4f}" if isinstance(loss, (int, float)) else str(loss)
        f_acc = f"{acc:.4f}" if isinstance(acc, (int, float)) else str(acc)
        
        self.table.add_row(str(epoch), f_loss, f_acc)
        
        # Auto-scroll table if too long (Rich table handles this by just growing, Live display handles rendering)
        # But if we want to show only last N rows, we might need to rebuild table. 
        # For now, let it grow.
        
        # Update progress description if epoch provided
        total_epochs = self.config.get("epochs")
        if total_epochs and isinstance(epoch, int):
            self.progress.update(self.task_id, total=total_epochs, completed=epoch)

    def set_status(self, status: str):
        self.progress.update(self.task_id, description=status)


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
        model_config = Config.get(f"ml.models.{model_name}", {})
        model = model_class(**model_config)
        # console.print(f"[blue]Loaded config for {model_name}:[/blue] {model_config}")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to instantiate {model_name}: {e}")
        raise typer.Exit(code=1)

    # Initialize Dashboard
    dashboard = TrainingDashboard(model_name, model_config)
    
    # Inject tracker into model
    # We check if set_tracker exists to support older models (though we just added it to BaseModel)
    if hasattr(model, "set_tracker"):
        model.set_tracker(dashboard)

    with Live(dashboard.layout, refresh_per_second=4, screen=True):
        
        # 1. Load Data
        dashboard.set_status("Loading data...")
        try:
            data = model.load_data()
        except Exception as e:
            console.print(f"[bold red]Error during load_data:[/bold red] {e}")
            raise typer.Exit(code=1)

        # 2. Transform
        dashboard.set_status("Transforming data...")
        try:
            data = model.transform(data)
        except Exception as e:
            console.print(f"[bold red]Error during transform:[/bold red] {e}")
            raise typer.Exit(code=1)

        # 3. Build
        dashboard.set_status("Building model architecture...")
        try:
            model.build()
        except Exception as e:
            console.print(f"[bold red]Error during build:[/bold red] {e}")
            raise typer.Exit(code=1)

        # 4. Fit
        dashboard.set_status(f"Training {model_name}...")
        try:
            model.fit(data)
            dashboard.set_status("[green]Training Completed[/green]")
            # Keep the display for a moment or wait for user?
            # With screen=True, it will disappear when context exits.
            # Maybe we shouldn't use screen=True if we want to keep history?
            # User said "sleek CLI output", screen=True gives a dashboard feel.
            # But "Clean table" usually implies persistence. 
            # Let's NOT use screen=True so it prints to terminal, but Live will rewrite.
            # If we want final output, we should print summary after Live context.
        except Exception as e:
            console.print(f"[bold red]Error during fit:[/bold red] {e}")
            raise typer.Exit(code=1)

    # Print summary after training
    console.print(f"\n[bold green]Training completed successfully for {model_name}![/bold green]")
    # We could print the final metrics table here again if we want persistence
    console.print(dashboard.table)
