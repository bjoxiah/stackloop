import logging
from pathlib import Path
from typing import Union
from pydantic_ai import Agent, ModelRetry, RunContext

from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider

from rich.console import Console
import typer

from stackloop.agent.models.agent_input import Deps
from stackloop.agent.models.agent_output import NoResult, OutputResult
from stackloop.agent.models.tools_param import FixFileParam, ReadFileParam
from stackloop.agent.prompt import system_prompt
from stackloop.agent.tools.fix_file import fix_file_operation
from stackloop.agent.tools.read_file import read_file_operation
from stackloop.agent.tools.run_code import run_code_operation
from stackloop.cli.display import display_message
from stackloop.core.agent_config import get_api_key

class AgentSetup:
    """
    Factory/configuration class for building a StackLoop debugging Agent.

    Usage:
        setup = AgentSetup(provider="openai", model_name="gpt-4o", console=console, log=logger)
        agent = setup.agent
    """

    def __init__(self, provider: str, model_name: str, console: Console, log: logging.Logger):
        """
        Initialize the agent setup and build the debugging agent.

        Args:
            provider (str): The LLM provider name ("groq", "openai", "anthropic").
            model_name (str): The specific model identifier for the provider.
            console (Console): Rich console for user-facing output.
            log (logging.Logger): Logger for internal debugging.
        """

        self.console = console
        self.log = log
        api_key = get_api_key(provider, console)

        model_lookup = {
            "groq": lambda: GroqModel(model_name, provider=GroqProvider(api_key=api_key)),
            "openai": lambda: OpenAIChatModel(model_name, provider=OpenAIProvider(api_key=api_key)),
            "anthropic": lambda: AnthropicModel(model_name, provider=AnthropicProvider(api_key=api_key)),
        }

        if provider not in model_lookup:
            display_message(console, f"[red]Unsupported provider: {provider}[/red]")
            raise typer.Exit()

        model = model_lookup[provider]()

        # --------------------------------------
        # Create the agent and attach to instance
        # --------------------------------------
        self.agent = Agent(
            model=model,
            name="StackLoop-Debugging-Agent",
            output_type=Union[OutputResult, NoResult],
            retries=2, # Guardrail
            end_strategy="early",
            system_prompt=system_prompt(),
        )

        # Register tools
        self._register_tools()

    # --------------------------------------
    # Tool registration isolated in a method
    # --------------------------------------
    def _register_tools(self):
        """Register all pydantic-ai tools for this agent."""

        log = self.log
        agent = self.agent

        @agent.tool
        def run_code(ctx: RunContext[Deps]) -> str:
            """
            Execute the target script and return JSON execution results.

            Usage:
                run_code()
            """
            log.info("🔧 Run Code Tool Called")
            return run_code_operation(ctx, log)

        @agent.tool
        def read_file(ctx: RunContext[Deps], data: ReadFileParam) -> str:
            """
            Read the contents of files using absolute paths.

            Args:
                data (ReadFileParam): File descriptors with absolute paths.

            Raises:
                ModelRetry: If any path is not absolute.

            Returns:
                str: JSON string of file contents.
            """
            log.info("🔧 Read File Tool Called")

            errors = [
                f"File not absolute path: {item.file_path}"
                for item in data.files
                if not Path(item.file_path).is_absolute()
            ]

            if errors:
                raise ModelRetry("Invalid absolute file paths:\n" + "\n".join(errors))

            return read_file_operation(ctx, data, log)

        @agent.tool
        def fix_file(ctx: RunContext[Deps], data: FixFileParam) -> str:
            """
            Apply code fixes to files.

            Args:
                data (FixFileParam): File fix definitions.

            Raises:
                ModelRetry: If any path is not absolute.

            Returns:
                str: JSON result of the applied fixes.
            """
            log.info("🔧 Fix File Tool Called")

            errors = [
                f"File not absolute path: {item.file_path}"
                for item in data.fixes
                if not Path(item.file_path).is_absolute()
            ]

            if errors:
                log.error("\n".join(errors))
                raise ModelRetry("Invalid file paths:\n" + "\n".join(errors))

            return fix_file_operation(data, log)
