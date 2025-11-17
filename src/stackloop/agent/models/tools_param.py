from pydantic import BaseModel, Field

from stackloop.agent.models.tools_output import ReadFileBase


class ReadFileParam(BaseModel):
    files: list[ReadFileBase] = Field(description="List of files to read.")


class FixFileBase(BaseModel):
    error_type: str = Field(description='Error type (e.g., SyntaxError, ImportError, RuntimeError).')
    file_path: str = Field(description='Absolute Path to the file that needs to be fixed')
    corrected_content: str = Field(description='The corrected full code content of the file')

class FixFileParam(BaseModel):
    fixes: list[FixFileBase] = Field(description='List of file fixes to apply')