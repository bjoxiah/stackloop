import json
from pathlib import Path
from pydantic_ai import RunContext
from stackloop.agent.models.agent_input import Deps
import logging

from stackloop.agent.models.tools_output import RunCodeResult
from stackloop.agent.utils.run_application import run_application


def run_code_operation(ctx: RunContext[Deps], log: logging.Logger) -> str:
    
    log.info(f"\n🔧 Run Code Operation Called\n")
    
    log.info(f"\n🔧 Running: {ctx.deps.script} in {ctx.deps.path}\n")
    
    result = run_application(ctx.deps.script, Path(ctx.deps.path), log)
    
    log.info(f"\nRun Application Result:\n{result}\n\n")
    
    return result.model_dump_json()