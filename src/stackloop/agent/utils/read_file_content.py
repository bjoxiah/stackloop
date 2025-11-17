import logging
from pathlib import Path


def read_file_content(file_path: Path, log: logging.Logger) -> str:
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        log.error(f"\nFailed to read file ==> {file_path}: \n{e}\n")
        return None