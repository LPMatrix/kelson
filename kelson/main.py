import typer
from rich.console import Console
from kelson.commands import new, make, train
from kelson.core.config import Config
from kelson.core.container import Container, resolve
from pathlib import Path

app = typer.Typer(
    name="kelson",
    help="A highly opinionated, batteries-included framework for Machine Learning.",
    add_completion=False,
    no_args_is_help=True
)

console = Console()

@app.callback()
def main(ctx: typer.Context):
    """
    Kelson CLI entry point.
    """
    # Bootstrap application if not creating a new project
    if ctx.invoked_subcommand != "new":
        if Path("config").exists():
            Config.load()
            
            # Bind data loader if defined in config
            loader_path = Config.get("data.loader")
            if loader_path:
                try:
                    # Bind as a factory
                    Container.bind("data_loader", lambda: resolve(loader_path))
                except Exception as e:
                    # Don't crash the CLI, just warn
                    # console.print(f"[yellow]Warning:[/yellow] Could not bind 'data.loader': {e}")
                    pass

# Register commands
app.command(name="new")(new.create_project)
app.command(name="make:model")(make.make_model)
app.command(name="train")(train.train_model)

if __name__ == "__main__":
    app()
