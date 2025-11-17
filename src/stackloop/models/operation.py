from dataclasses import dataclass
import logging
from pydantic_ai import Agent
from rich.console import Console

from stackloop.models.session_config import SessionConfig

@dataclass
class AgentOperation:
    session: SessionConfig
    agent: Agent
    log: logging.Logger
    console: Console