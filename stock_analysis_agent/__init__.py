"""
Stock Analysis Deep Agent

A Deep Agent implementation for stock market analysis using the Deep Agents framework.

Features:
- Planning tool for complex multi-step analyses
- File system for saving reports and data
- Sub-agents for specialized research tasks
- Expert stock analysis system prompt
- Real-time stock data tools
- Multi-provider support via LangChain 1.0 (14+ LLM providers)
"""

from .agent import (
    create_stock_analysis_agent,
    run_analysis,
    get_supported_providers,
    list_providers,
    SUPPORTED_PROVIDERS
)
from .tools import STOCK_TOOLS
from .prompts import STOCK_ANALYST_PROMPT, RESEARCH_SUBAGENT_PROMPT

__version__ = "1.0.0"

__all__ = [
    "create_stock_analysis_agent",
    "run_analysis",
    "get_supported_providers",
    "list_providers",
    "SUPPORTED_PROVIDERS",
    "STOCK_TOOLS",
    "STOCK_ANALYST_PROMPT",
    "RESEARCH_SUBAGENT_PROMPT"
]
