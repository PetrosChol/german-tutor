"""
Tools for Your Agent

This module defines the tools your agent can use. Each tool should:
1. Have a clear, focused purpose
2. Include comprehensive docstrings
3. Handle errors gracefully
4. Return structured data (preferably JSON)

Replace these example tools with your domain-specific tools.
"""

import json
from typing import Optional
from langchain_core.tools import tool


@tool
def example_tool_1(query: str) -> str:
    """
    Brief description of what this tool does.

    Use this tool when you need to [describe use case].

    Args:
        query: Description of the query parameter

    Returns:
        JSON string with results or error information

    Example:
        example_tool_1("test query") -> {"success": True, "data": "result"}
    """
    try:
        # Replace with your actual logic
        result = f"Processed: {query}"

        return json.dumps({
            "success": True,
            "data": result,
            "query": query
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "query": query
        }, indent=2)


@tool
def example_tool_2(
    param1: str,
    param2: Optional[int] = 10
) -> str:
    """
    Another example tool with multiple parameters.

    Use this when you need to [describe use case].

    Args:
        param1: Required parameter description
        param2: Optional parameter description (default: 10)

    Returns:
        JSON string with results

    Example:
        example_tool_2("test", 5) -> {"success": True, "count": 5}
    """
    try:
        # Your logic here
        result = {
            "param1": param1,
            "param2": param2,
            "processed": True
        }

        return json.dumps({
            "success": True,
            "data": result
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


# Export all tools
TOOLS = [
    example_tool_1,
    example_tool_2,
]


# Optional: Tool categories for different agent types
BASIC_TOOLS = [example_tool_1]
ADVANCED_TOOLS = [example_tool_1, example_tool_2]
