import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from pyfiglet import Figlet
from importlib.metadata import version, PackageNotFoundError


def get_package_version(package_name: str) -> str:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "unknown"


def display_welcome(console: Console):
    """Show a beautiful, padded ASCII banner with rich formatting."""
    console.clear()
    
    # ASCII Banner
    fig = Figlet(font="slant")
    ascii_art = fig.renderText("StackLoop")
    banner = f"[bold magenta]{ascii_art}[/bold magenta]"
    
    # Description Panel
    desc_text = Text(
        "⚙️  AI-powered debugging agent that runs, analyzes, and fixes your code.\n",
        style="bright_cyan",
        justify="left"
    )
    
    panel = Panel.fit(
        desc_text,
        border_style="bright_magenta",
        title="[bold cyan]Welcome to StackLoop[/bold cyan]",
        subtitle=f"v{get_package_version('stackloop')}",
        padding=(1, 4),
        box=box.ROUNDED,
    )
    
    console.print("\n\n")
    console.print(banner)
    time.sleep(0.1)
    console.print(panel)
    console.print("\n")
    
def display_message(console: Console, message: str):
    console.print(f"{message}")
    
def display_diagnosis(console: Console, message: str, style: str = 'bright_white'):
    diagnosis_text = Text(message, style)
    panel = Panel.fit(
        diagnosis_text,
        title="[bold cyan]🤖 AI Diagnosis[/bold cyan]",
        border_style="cyan",
        padding=(1, 4),
        box=box.ROUNDED,
    )
    console.print("\n")
    console.print(panel)
    console.print("\n")
    
def display_success(console: Console, message: str, style: str = 'bright_white'):
    success_text = Text(message, style)
    panel = Panel.fit(
        success_text,
        title="[bold green]🎉 Success [/bold green]",
        border_style="cyan",
        padding=(1, 4),
        box=box.ROUNDED
    )
    console.print("\n")
    console.print(panel)
    console.print("\n")
