"""
Research Assistant Deep Agent

A comprehensive research agent powered by Deep Agents and LangChain 1.0.
"""

from .agent import create_research_assistant, conduct_research
from .tools import RESEARCH_TOOLS
from .prompts import RESEARCH_ASSISTANT_PROMPT

__version__ = "1.0.0"

__all__ = [
    "create_research_assistant",
    "conduct_research",
    "RESEARCH_TOOLS",
    "RESEARCH_ASSISTANT_PROMPT"
]
