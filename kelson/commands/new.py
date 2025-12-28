import typer
from rich.console import Console
from kelson.core.scaffold import ProjectScaffolder

console = Console()

def create_project(project_name: str = typer.Argument(..., help="The name of the new ML project")):
    """
    Create a new Kelson project with the standard directory structure.
    """
    console.print(f"[bold green]Creating a new Kelson project: [white]{project_name}[/white]...[/bold green]")
    
    scaffolder = ProjectScaffolder(project_name)
    scaffolder.build()
    
    console.print(f"\n[bold green]Success![/bold green] Project [bold white]{project_name}[/bold white] created.")
    console.print(f"cd {project_name} && pip install -e .")
