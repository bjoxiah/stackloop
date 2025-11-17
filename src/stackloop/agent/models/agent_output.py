from enum import Enum
from pydantic import BaseModel, Field

class ErrorCategory(str, Enum):
    """Categories of errors that determine if LLM can fix them."""
    AUTO_FIXABLE = "auto_fixable"  # LLM can fix automatically
    MANUAL_REQUIRED = "manual_required"  # Requires human intervention
    UNKNOWN = "unknown"  # Needs analysis
 
class OutputFile(BaseModel):
    content: str = Field(description='Brief Summary of the error found')
    file_path: str = Field(description="Absolute path to the file")
    error_message: str = Field(description="The actual error from execution")
    error_type: str = Field(description="Classified error type")
    error_category: ErrorCategory = Field(description="Whether error is auto-fixable or requires manual intervention")
    fix_applied: bool = Field(description="Whether a fix was applied")
    fix_explanation: str = Field(description="What was fixed or why manual intervention is needed")

class OutputResult(BaseModel):
    files: list[OutputFile] = Field(description='List of files that were fixed with their respective fixes')
    

class NoResult(BaseModel):
    message: str = Field(description='Message indicating no results were found')
    