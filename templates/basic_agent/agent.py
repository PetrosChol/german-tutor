"""
Your Custom Deep Agent

This module creates your domain-specific Deep Agent using the Deep Agents framework.

Usage:
    from your_agent import create_agent, run_task

    agent = create_agent()
    result = run_task("Your task here", agent)
"""

import os
from typing import Optional, List, Dict, Any
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import BaseTool

# Import your custom components
from tools import TOOLS
from prompts import MAIN_AGENT_PROMPT, SUBAGENT_PROMPT


# Supported LLM providers configuration
SUPPORTED_PROVIDERS = {
    "anthropic": {"default_model": "claude-sonnet-4-20250514"},
    "openai": {"default_model": "gpt-4o"},
    "google_genai": {"default_model": "gemini-2.0-flash"},
    "groq": {"default_model": "llama-3.3-70b-versatile"},
    "ollama": {"default_model": "llama3.2"},
}


def create_agent(
    model: Optional[str] = None,
    provider: Optional[str] = None,
    temperature: float = 0.1,
    workspace_dir: str = "./workspace",
    additional_tools: Optional[List[BaseTool]] = None,
    enable_subagents: bool = False,
    **model_kwargs
) -> Any:
    """
    Create your custom Deep Agent.

    Args:
        model: Model name (e.g., "gpt-4o", "claude-sonnet-4-20250514")
               Can also use "provider:model" format (e.g., "openai:gpt-4o")
        provider: LLM provider name (optional, auto-detected from model)
        temperature: Model temperature for response randomness (0.0-1.0)
        workspace_dir: Directory for agent's file system workspace
        additional_tools: Extra tools to add beyond default tools
        enable_subagents: Whether to enable sub-agent functionality
        **model_kwargs: Additional parameters to pass to the model

    Returns:
        Configured Deep Agent ready to use

    Examples:
        # Basic usage with default provider (Anthropic)
        >>> agent = create_agent()

        # With specific provider
        >>> agent = create_agent(model="gpt-4o")
        >>> agent = create_agent(provider="google_genai", model="gemini-2.0-flash")

        # With custom parameters
        >>> agent = create_agent(
        ...     model="claude-sonnet-4-20250514",
        ...     temperature=0.3,
        ...     max_tokens=4096
        ... )
    """

    # Create workspace directory
    os.makedirs(workspace_dir, exist_ok=True)

    # Handle provider:model format
    if model and ":" in model:
        provider_from_model, model_name = model.split(":", 1)
        provider = provider or provider_from_model
        model = model_name

    # Set defaults
    if not provider:
        provider = "anthropic"
    if not model:
        model = SUPPORTED_PROVIDERS[provider]["default_model"]

    # Initialize the model using LangChain 1.0's unified API
    try:
        chat_model = init_chat_model(
            model=model,
            model_provider=provider,
            temperature=temperature,
            **model_kwargs
        )
        print(f"✓ Initialized {provider} model: {model}")

    except Exception as e:
        raise RuntimeError(
            f"Failed to initialize {provider} model '{model}'.\n"
            f"Error: {e}\n\n"
            f"Make sure you have:\n"
            f"1. Installed the provider package: pip install langchain-{provider}\n"
            f"2. Set the API key in your environment"
        )

    # Combine tools
    tools = TOOLS.copy()
    if additional_tools:
        tools.extend(additional_tools)

    # Configure sub-agents (optional)
    subagents = []
    if enable_subagents:
        subagents = [{
            "name": "specialist",
            "description": (
                "Use this sub-agent for specialized tasks that require "
                "deep focus and detailed work. Good for: comprehensive research, "
                "detailed analysis, data processing."
            ),
            "prompt": SUBAGENT_PROMPT,
            "tools": tools,
            "model": chat_model  # Use same model for consistency
        }]

    # Create the Deep Agent
    agent = create_deep_agent(
        model=chat_model,
        tools=tools,
        system_prompt=MAIN_AGENT_PROMPT,
        subagents=subagents,

        # Configure the file system middleware
        filesystem_kwargs={
            "workspace_dir": workspace_dir,
            "description": (
                "Use the file system to save your work, analysis, and reports. "
                "This helps manage context and preserve important findings. "
                "Organize files in subdirectories for better structure."
            )
        },

        # Configure the todo list middleware
        todolist_kwargs={
            "description": (
                "Use write_todos to plan complex, multi-step tasks. "
                "Break tasks into clear, actionable steps and track your progress. "
                "Update todos as you complete each step."
            )
        }
    )

    return agent


def run_task(
    task: str,
    agent: Optional[Any] = None,
    verbose: bool = True,
    save_response: bool = False,
    response_file: Optional[str] = None
) -> str:
    """
    Execute a task using the agent.

    Args:
        task: The task description/question
        agent: Pre-configured agent (creates new one if None)
        verbose: Whether to print the response
        save_response: Whether to save response to a file
        response_file: Custom filename for saved response

    Returns:
        The agent's response as a string

    Examples:
        >>> response = run_task("Analyze data for Q4 2024")
        >>> response = run_task("Research topic X", save_response=True)
    """

    # Create agent if not provided
    if agent is None:
        agent = create_agent()

    # Execute the task
    result = agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })

    # Extract response
    messages = result.get("messages", [])
    if not messages:
        return "No response generated"

    final_message = messages[-1]
    response = final_message.content if hasattr(final_message, "content") else str(final_message)

    # Display response
    if verbose:
        print("\n" + "="*80)
        print("AGENT RESPONSE")
        print("="*80)
        print(response)
        print("="*80 + "\n")

    # Save response if requested
    if save_response:
        filename = response_file or "response.txt"
        with open(filename, "w") as f:
            f.write(response)
        if verbose:
            print(f"📝 Response saved to {filename}\n")

    return response


# CLI interface for direct execution
if __name__ == "__main__":
    import sys

    print("\n🤖 Your Custom Deep Agent\n")

    # Check for API keys
    has_key = any([
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("OPENAI_API_KEY"),
        os.getenv("GOOGLE_API_KEY"),
    ])

    if not has_key:
        print("⚠️  No API key found!")
        print("\nPlease set an API key:")
        print("  export ANTHROPIC_API_KEY='your-key'  # For Claude")
        print("  export OPENAI_API_KEY='your-key'     # For GPT-4")
        print("  export GOOGLE_API_KEY='your-key'     # For Gemini")
        sys.exit(1)

    # Create agent
    print("Creating agent...")
    try:
        agent = create_agent()
        print("✅ Agent ready!\n")
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        sys.exit(1)

    # Interactive mode or single command
    if len(sys.argv) > 1:
        # Execute command from arguments
        task = " ".join(sys.argv[1:])
        print(f"Task: {task}\n")
        run_task(task, agent=agent)
    else:
        # Interactive mode
        print("Interactive mode - Enter your tasks (Ctrl+C to exit)")
        print("-" * 80)

        try:
            while True:
                task = input("\n📋 Task: ").strip()
                if not task:
                    continue

                run_task(task, agent=agent)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
