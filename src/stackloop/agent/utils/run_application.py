import logging
from pathlib import Path
import shlex
import subprocess
import time

from stackloop.agent.models.tools_output import RunCodeResult


def run_application(script: str, work_dir: Path, log: logging.Logger) -> RunCodeResult:
    try:
        # Run in a separate process
        start_time = time.time()    
        result = subprocess.Popen(
            shlex.split(script),
            cwd=work_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = result.communicate()
        duration = time.time() - start_time
        
        return RunCodeResult(
            success=result.returncode == 0,
            stdout=stdout,
            stderr=stderr,
            execution_time=duration
        )
    except Exception as e:
        log.error(f"\nFailed to run code ==> {script} in {work_dir.as_posix()}: \n{e}\n")
        return RunCodeResult(
            success=False,
            stdout="",
            stderr=str(e),
            execution_time=0.0
        )