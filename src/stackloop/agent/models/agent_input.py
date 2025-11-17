from pydantic import BaseModel, Field


class Deps(BaseModel):
    script: str = Field(description='The script to run')
    path: str = Field(description='The project directory path')