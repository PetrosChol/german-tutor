"""
Deep Agent Template - Basic

A template for building custom Deep Agents with LangChain 1.0.
"""

from .agent import create_agent, run_task
from .tools import TOOLS
from .prompts import MAIN_AGENT_PROMPT, SUBAGENT_PROMPT

__version__ = "1.0.0"

__all__ = [
    "create_agent",
    "run_task",
    "TOOLS",
    "MAIN_AGENT_PROMPT",
    "SUBAGENT_PROMPT"
]
