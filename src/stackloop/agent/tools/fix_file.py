import json
import logging
from pathlib import Path

from stackloop.agent.models.tools_output import FixFileResult
from stackloop.agent.models.tools_param import FixFileParam
from stackloop.agent.utils.update_file_content import update_file_content


def fix_file_operation(data: FixFileParam, log: logging.Logger) -> str:
    log.info(f"\n🔧 Fix File Operation Called\n")
    
    results: list[FixFileResult] = []
    for item in data.fixes:
        log.info(f"\n🔧 Fixing File: {item.file_path} with error type: {item.error_type}\n")
        log.info(f"\n Updating File {item.file_path} with corrected content\n")
        update_file_content(Path(item.file_path), item.corrected_content, log)
        results.append(FixFileResult(
            file_path = item.file_path,
            fix_applied=True
        ))
        
    log.info(f"\nFix File Results: \n{results}\n")    
    return json.dumps([r.model_dump() for r in results], indent=2)
