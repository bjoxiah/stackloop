import json
import logging
from pathlib import Path
from pydantic_ai import RunContext

from stackloop.agent.models.agent_input import Deps
from stackloop.agent.models.tools_output import ReadFileResult
from stackloop.agent.models.tools_param import ReadFileParam
from stackloop.agent.utils.read_file_content import read_file_content


def read_file_operation(ctx: RunContext[Deps], data: ReadFileParam, log: logging.Logger) -> str:
    log.info(f"\n🔧 Read File Operation Called\n")
    results: list[ReadFileResult] = []
    for item in data.files:
        log.info(f"\n🔧Reading file: \n{item.file_path}\n")
        content = read_file_content(Path(item.file_path), log)
        if content is None:
            continue
        
        results.append(ReadFileResult(
            file_path=item.file_path,
            error_in_file=item.error_in_file,
            error_type=item.error_type,
            file_content=content
        ))
    
    log.info(f"\nRead File Results: \n{results}\n")
    return json.dumps([r.model_dump() for r in results], indent=2)