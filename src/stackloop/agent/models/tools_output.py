
from pydantic import BaseModel, Field, field_validator
from pathlib import Path


class RunCodeResult(BaseModel):
    """Result of running the application"""
    success: bool = Field(description='Did the program run successfully?')
    stdout: str = Field(description='Standard output of the program')
    stderr: str = Field(description='Standard error of the program')
    execution_time: float = Field(description='Time taken to execute the program in seconds')
    
class ReadFileBase(BaseModel):
    file_path: str = Field(description="Absolute path to the file to read.")
    error_in_file: str = Field(description="The error message associated with this file.")
    error_type: str = Field(description="Error type (e.g., SyntaxError, ImportError, RuntimeError).")
    
    @field_validator("file_path")
    def ensure_absolute(cls, v: str):
        if not Path(v).is_absolute():
            raise ValueError(f"file_path must be absolute. Got: {v}")
        return v
    
class ReadFileResult(ReadFileBase):
    file_content: str = Field(description="The full, original file contents.")
    
class FixFileResult(BaseModel):
    file_path: str = Field(description='Absolute Path to the file that was fixed')
    fix_applied: bool = Field(description='Whether a fix was applied to the file successfully')
    
    

