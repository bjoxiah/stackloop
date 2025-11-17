from typing import Union
from pydantic_ai import ModelMessage, RunUsage, UsageLimits
from rich.status import Status

from stackloop.agent.models.agent_input import Deps
from stackloop.agent.models.agent_output import NoResult, OutputResult
from stackloop.cli.display import display_diagnosis, display_message
from stackloop.models.operation import AgentOperation


async def run_agent_operation(
    data: AgentOperation
) -> Union[OutputResult, NoResult, None]:

    try:
        usage_limits = UsageLimits(request_limit=15) # Guardrails
        message_history: list[ModelMessage] | None = None
        usage: RunUsage = RunUsage()

        display_message(
            data.console,
            f"\n[dim]💡 Starting Fixer Agent For Script: {data.session.script} in path: {data.session.working_directory}[/dim]\n"
        )

        data.log.info(
            f"\nStarting Fixer Agent for script: {data.session.script} in path: {data.session.working_directory}\n"
        )

        data.session.modified_files = []

        # =========================
        #  ADD SPINNER HERE
        # =========================
        with Status(
            "[cyan]Analyzing and fixing your application...[/cyan]",
            console=data.console,
            spinner="dots"
        ) as status:

            while True:
                status.update(f"[cyan] AI agent working on the next iteration... [/cyan]\n\n")

                result = await data.agent.run(
                    user_prompt="Fix the errors in the codebase",
                    deps=Deps(
                        script=data.session.script,
                        path=data.session.working_directory.as_posix()
                    ),
                    message_history=message_history,
                    usage=usage,
                    usage_limits=usage_limits
                )

                data.log.info(f"\nAgent Output Result: \n{result.output}\n")

                if isinstance(result.output, OutputResult):
                    status.stop()
                    return result.output

                elif isinstance(result.output, NoResult):
                    status.stop()
                    return result.output

                else:
                    message_history = result.all_messages(
                        output_tool_return_content='Please try again'
                    )

    except Exception as e:
        display_diagnosis(data.console, f"\nError during agent operation: \n{e}\n", "bright_yellow")
        data.log.error(f"\nError during agent operation ==> : \n{e}\n")
        return None
