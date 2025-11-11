"""
Stock Analysis Deep Agent

This module creates a Deep Agent for stock market analysis using the Deep Agents framework.
The agent is equipped with:
1. Planning tool (TodoListMiddleware) - for breaking down complex analyses
2. File system backend (FilesystemMiddleware) - for saving reports and data
3. Sub-agents (SubAgentMiddleware) - for specialized research tasks
4. Detailed system prompt - for expert stock analysis behavior
"""

import os
from typing import Optional
from deepagents import create_deep_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from stock_analysis_agent.tools import STOCK_TOOLS
from stock_analysis_agent.prompts import STOCK_ANALYST_PROMPT, RESEARCH_SUBAGENT_PROMPT


def create_stock_analysis_agent(
    model_provider: str = "anthropic",
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    workspace_dir: str = "./stock_analysis_workspace"
):
    """
    Create a Deep Agent specialized for stock market analysis.

    Args:
        model_provider: The LLM provider to use ("anthropic" or "openai")
        model_name: Specific model name (e.g., "claude-sonnet-4-20250514", "gpt-4")
        api_key: API key for the model provider (if not set in environment)
        workspace_dir: Directory for the agent's file system workspace

    Returns:
        A LangGraph agent configured for stock analysis

    Example:
        >>> agent = create_stock_analysis_agent(model_provider="anthropic")
        >>> result = agent.invoke({
        ...     "messages": [{"role": "user", "content": "Analyze Apple stock"}]
        ... })
    """

    # Create workspace directory if it doesn't exist
    os.makedirs(workspace_dir, exist_ok=True)

    # Set up the model
    if model_provider == "anthropic":
        if api_key:
            os.environ["ANTHROPIC_API_KEY"] = api_key

        model = ChatAnthropic(
            model=model_name or "claude-sonnet-4-20250514",
            temperature=0.1  # Lower temperature for more consistent analysis
        )
    elif model_provider == "openai":
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        model = ChatOpenAI(
            model=model_name or "gpt-4o",
            temperature=0.1
        )
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")

    # Define the research sub-agent for deep analysis tasks
    research_subagent = {
        "name": "research_agent",
        "description": (
            "Use this agent for deep research tasks like sector analysis, "
            "competitive analysis, or processing large amounts of stock data. "
            "This agent has the same tools but is optimized for thorough research."
        ),
        "prompt": RESEARCH_SUBAGENT_PROMPT,
        "tools": STOCK_TOOLS,
        "model": model  # Use the same model for consistency
    }

    # Create the deep agent with all components
    agent = create_deep_agent(
        model=model,
        tools=STOCK_TOOLS,
        system_prompt=STOCK_ANALYST_PROMPT,
        subagents=[research_subagent],
        # Configure the file system workspace
        filesystem_kwargs={
            "workspace_dir": workspace_dir,
            "description": (
                "File system for saving stock analysis reports, raw data, "
                "and research findings. Use this to organize your work."
            )
        },
        # Configure todo list for planning
        todolist_kwargs={
            "description": (
                "Use this to plan complex stock analyses by breaking them "
                "into manageable steps. Update as you complete each step."
            )
        }
    )

    return agent


def run_analysis(query: str, agent=None, verbose: bool = True):
    """
    Run a stock analysis query using the agent.

    Args:
        query: The analysis question or request
        agent: Pre-configured agent (creates new one if None)
        verbose: Whether to print intermediate steps

    Returns:
        The agent's response
    """
    if agent is None:
        agent = create_stock_analysis_agent()

    # Invoke the agent with the query
    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config={"configurable": {"thread_id": "stock_analysis_session"}}
    )

    # Extract the final response
    messages = result.get("messages", [])
    if messages:
        final_message = messages[-1]
        response = final_message.content if hasattr(final_message, "content") else str(final_message)

        if verbose:
            print("\n" + "="*80)
            print("STOCK ANALYSIS AGENT RESPONSE")
            print("="*80)
            print(response)
            print("="*80 + "\n")

        return response

    return "No response generated"


if __name__ == "__main__":
    """
    Example usage and testing
    """
    import sys

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: No API key found in environment variables.")
        print("Please set ANTHROPIC_API_KEY or OPENAI_API_KEY")
        print("\nExample:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        print("  python agent.py")
        sys.exit(1)

    # Create the agent
    print("🤖 Creating Stock Analysis Deep Agent...")
    agent = create_stock_analysis_agent()
    print("✅ Agent created successfully!\n")

    # Example queries
    example_queries = [
        "What's the current price of Apple stock?",
        # "Compare Tesla and General Motors",
        # "Analyze NVIDIA's performance over the last year"
    ]

    # Run a simple analysis
    query = example_queries[0]
    print(f"📊 Running analysis: {query}\n")

    response = run_analysis(query, agent=agent)

    print("\n✅ Analysis complete!")
    print("\nℹ️  Check the 'stock_analysis_workspace' directory for any saved reports.")
