import logging
from pathlib import Path


def update_file_content(file_path: Path, content: str, log: logging.Logger) -> str:
    try:
        # Create a backup before updating
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        with open(backup_path, 'w') as backup_file:
            with open(file_path, 'r') as original_file:
                backup_file.write(original_file.read())
                
        # Write the new content to the original file
        with open(file_path, 'w') as f:
            f.write(content)
        return content
    except Exception as e:
        log.error(f"\nFailed to update file ==> {file_path}: \n{e}\n")
        return None