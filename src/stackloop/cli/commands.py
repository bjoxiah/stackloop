import asyncio
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from dotenv import load_dotenv

from stackloop.agent.models.agent_output import NoResult, OutputResult
from stackloop.agent.setup import AgentSetup
from stackloop.core.agent_config import select_model, select_provider
from stackloop.core.agent_operation import run_agent_operation
from stackloop.models.operation import AgentOperation
from stackloop.core.debug_session import DebugSession
from stackloop.cli.display import display_diagnosis, display_message, display_success, display_welcome, get_package_version
from stackloop.cli.prompts import (
    confirm_sync_back, get_runtime_choice, get_script_command, resolve_directory
)
import logging


app = typer.Typer(help="StackLoop - AI-powered debugging agent", no_args_is_help=True)
console = Console()

def version_callback(value: bool):
    """Display StackLoop version when --version or -v is used."""
    if value:
        v = get_package_version("stackloop")
        if v != "unknown":
            display_message(console, f"\n[bold cyan]StackLoop version {v}[/bold cyan]\n")
        else:
            display_message(console, f"\n[yellow]StackLoop version unknown[/yellow]\n")
        raise typer.Exit()

@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, 
        "--version", 
        "-v", 
        callback=version_callback, 
        is_eager=True, 
        help="Show version and exit"
    )
):
    """StackLoop - AI-powered debugging agent"""
    if ctx.invoked_subcommand is None:
        display_message(console, ctx.get_help())
        raise typer.Exit()


@app.command("run")
def run(directory: Optional[Path] = typer.Argument(None, help="Project root directory")):
    """Run StackLoop to debug and fix your app automatically."""
    try:
        # -----------------------------
        # Setup
        # -----------------------------
        display_welcome(console)
        root_dir = resolve_directory(directory)
        load_dotenv(root_dir / ".env")

        if not root_dir.exists():
            display_message(console, f"\n[red]❌ Directory not found: {root_dir}[/red]\n")
            raise typer.Exit()

        # AI Agent setup
        provider = select_provider()
        model_name = select_model(provider, console)
        display_message(console, f"\n[dim]📁 Project directory: {root_dir}[/dim]\n")

        runtime = get_runtime_choice()
        script = get_script_command(runtime)

        # Session and config
        session = DebugSession(root_dir, runtime, script)
        config = session.setup(console)

        # Logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            filename=f"{config.working_directory}/agent.log",
            filemode="a",
        )

        # -----------------------------
        # Initialize fixer agent
        # -----------------------------
        fixer_agent = AgentSetup(provider, model_name, console, logging.getLogger("stackloop"))

        # -----------------------------
        # Run agent
        # -----------------------------
        display_message(console, f"\n[bold yellow]🚀 Running your application...[/bold yellow]\n")

        result = asyncio.run(
            run_agent_operation(
                AgentOperation(
                    session=config,
                    agent=fixer_agent.agent,
                    log=logging.getLogger("stackloop"),
                    console=console,
                )
            )
        )

        # -----------------------------
        # Process result
        # -----------------------------
        if isinstance(result, OutputResult):
            fixed_any = False
            for item in result.files:
                if item.fix_applied:
                    fixed_any = True
                    if item.file_path not in config.modified_files:
                        display_message(console, f"\n[dim]📝 Fixed file: {item.file_path}[/dim]\n")
                        config.modified_files.append(item.file_path)

            # Save session config if any files were modified
            if fixed_any:
                session._save_config(config, console)
                display_message(console, f"\n[bold yellow]🔄 Files were fixed in the working directory.[/bold yellow]\n")
            else:
                # No fixes applied, show errors
                errors = [f"{file.file_path}: {file.error_message} - {file.fix_explanation}" for file in result.files if hasattr(file, "error_message") and hasattr(file, "fix_explanation")]
                if errors:
                    display_diagnosis(console, f"\n".join(errors) + "\n", "bright_yellow")
                    return

            # Ask user whether to sync back to root
            if fixed_any and confirm_sync_back():
                session.create_backup_for_root(console, config)
                session.sync_back_to_root(console, config)
                display_success(console, f"\n✨ All done! Your files have been updated.\n")
            elif fixed_any:
                display_success(console, f"\n💡 Fixed files are in: {session.work_dir}\n")

        elif isinstance(result, NoResult):
            display_success(console, f"\n{result.message}\n")
        else:
            display_diagnosis(console, f"\nStackLoop could not complete the operation. Find detailed errors in the log file.\n", "bright_yellow")

    except KeyboardInterrupt:
        display_message(console, f"\n[yellow]⚠️ Cancelled by user [/yellow]\n")
        raise typer.Exit()
    except typer.Exit:
        raise
    except Exception as e:
        display_diagnosis(console, f"\nError: {e}\n", "bright_yellow")
        return
