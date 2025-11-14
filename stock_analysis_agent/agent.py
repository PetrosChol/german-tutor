"""
Stock Analysis Deep Agent

This module creates a Deep Agent for stock market analysis using the Deep Agents framework.
The agent is equipped with:
1. Planning tool (TodoListMiddleware) - for breaking down complex analyses
2. File system backend (FilesystemMiddleware) - for saving reports and data
3. Sub-agents (SubAgentMiddleware) - for specialized research tasks
4. Detailed system prompt - for expert stock analysis behavior

Uses LangChain 1.0's unified init_chat_model API for multi-provider support.
"""

import os
from typing import Optional, Dict, Any
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

from stock_analysis_agent.tools import STOCK_TOOLS
from stock_analysis_agent.prompts import STOCK_ANALYST_PROMPT, RESEARCH_SUBAGENT_PROMPT


# Supported LLM providers in LangChain 1.0
SUPPORTED_PROVIDERS = {
    "openai": {
        "env_var": "OPENAI_API_KEY",
        "default_model": "gpt-4o",
        "package": "langchain-openai",
        "examples": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "o1", "o3-mini"]
    },
    "anthropic": {
        "env_var": "ANTHROPIC_API_KEY",
        "default_model": "claude-sonnet-4-20250514",
        "package": "langchain-anthropic",
        "examples": ["claude-sonnet-4-20250514", "claude-opus-4-20250514", "claude-3-5-sonnet-20241022"]
    },
    "google_vertexai": {
        "env_var": "GOOGLE_APPLICATION_CREDENTIALS",
        "default_model": "gemini-2.0-flash",
        "package": "langchain-google-vertexai",
        "examples": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
    },
    "google_genai": {
        "env_var": "GOOGLE_API_KEY",
        "default_model": "gemini-2.0-flash",
        "package": "langchain-google-genai",
        "examples": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
    },
    "cohere": {
        "env_var": "COHERE_API_KEY",
        "default_model": "command-r-plus",
        "package": "langchain-cohere",
        "examples": ["command-r-plus", "command-r", "command"]
    },
    "groq": {
        "env_var": "GROQ_API_KEY",
        "default_model": "llama-3.3-70b-versatile",
        "package": "langchain-groq",
        "examples": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"]
    },
    "together": {
        "env_var": "TOGETHER_API_KEY",
        "default_model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "package": "langchain-together",
        "examples": ["meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", "mistralai/Mixtral-8x7B-Instruct-v0.1"]
    },
    "mistralai": {
        "env_var": "MISTRAL_API_KEY",
        "default_model": "mistral-large-latest",
        "package": "langchain-mistralai",
        "examples": ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"]
    },
    "fireworks": {
        "env_var": "FIREWORKS_API_KEY",
        "default_model": "accounts/fireworks/models/llama-v3p1-70b-instruct",
        "package": "langchain-fireworks",
        "examples": ["accounts/fireworks/models/llama-v3p1-70b-instruct"]
    },
    "ollama": {
        "env_var": None,  # Local, no API key needed
        "default_model": "llama3.2",
        "package": "langchain-ollama",
        "examples": ["llama3.2", "mistral", "phi3", "qwen2.5"]
    },
    "bedrock": {
        "env_var": "AWS_ACCESS_KEY_ID",  # Also needs AWS_SECRET_ACCESS_KEY
        "default_model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "package": "langchain-aws",
        "examples": ["anthropic.claude-3-5-sonnet-20241022-v2:0", "meta.llama3-1-70b-instruct-v1:0"]
    },
    "azure_openai": {
        "env_var": "AZURE_OPENAI_API_KEY",
        "default_model": "gpt-4o",
        "package": "langchain-openai",
        "examples": ["gpt-4o", "gpt-4-turbo"]
    },
    "deepseek": {
        "env_var": "DEEPSEEK_API_KEY",
        "default_model": "deepseek-chat",
        "package": "langchain-openai",  # DeepSeek uses OpenAI-compatible API
        "examples": ["deepseek-chat", "deepseek-coder"]
    },
    "xai": {
        "env_var": "XAI_API_KEY",
        "default_model": "grok-2-latest",
        "package": "langchain-xai",
        "examples": ["grok-2-latest", "grok-2-vision-latest"]
    },
    "perplexity": {
        "env_var": "PERPLEXITY_API_KEY",
        "default_model": "sonar-pro",
        "package": "langchain-community",
        "examples": ["sonar-pro", "sonar"]
    }
}


def create_stock_analysis_agent(
    model: Optional[str] = None,
    provider: Optional[str] = None,
    temperature: float = 0.1,
    api_key: Optional[str] = None,
    workspace_dir: str = "./stock_analysis_workspace",
    **model_kwargs
):
    """
    Create a Deep Agent specialized for stock market analysis.

    This function uses LangChain 1.0's unified init_chat_model API to support
    ALL major LLM providers with a single, consistent interface.

    Args:
        model: Model name to use. Can be:
            - Simple name: "gpt-4o", "claude-sonnet-4-20250514", "gemini-2.0-flash"
            - Provider-prefixed: "openai:gpt-4o", "anthropic:claude-sonnet-4-20250514"
            If not specified, uses the default model for the given provider.

        provider: LLM provider name. Supported providers:
            - openai: OpenAI GPT models
            - anthropic: Anthropic Claude models
            - google_vertexai: Google Gemini (Vertex AI)
            - google_genai: Google Gemini (direct API)
            - cohere: Cohere Command models
            - groq: Groq (fast inference)
            - together: Together AI
            - mistralai: Mistral AI
            - fireworks: Fireworks AI
            - ollama: Ollama (local models)
            - bedrock: AWS Bedrock
            - azure_openai: Azure OpenAI
            - deepseek: DeepSeek
            - xai: xAI Grok models
            - perplexity: Perplexity AI

            If not specified, LangChain will auto-detect from model name.

        temperature: Model temperature (0.0-1.0). Default: 0.1 for consistent analysis

        api_key: API key for the model provider (if not set in environment)

        workspace_dir: Directory for the agent's file system workspace

        **model_kwargs: Additional arguments passed to the model (e.g., max_tokens, top_p)

    Returns:
        A LangGraph agent configured for stock analysis

    Examples:
        # Using auto-detection
        >>> agent = create_stock_analysis_agent(model="gpt-4o")
        >>> agent = create_stock_analysis_agent(model="claude-sonnet-4-20250514")

        # Using explicit provider
        >>> agent = create_stock_analysis_agent(
        ...     provider="anthropic",
        ...     model="claude-sonnet-4-20250514"
        ... )

        # Using provider:model format
        >>> agent = create_stock_analysis_agent(model="openai:gpt-4o")
        >>> agent = create_stock_analysis_agent(model="google_vertexai:gemini-2.0-flash")

        # Using local models
        >>> agent = create_stock_analysis_agent(model="ollama:llama3.2")

        # With custom parameters
        >>> agent = create_stock_analysis_agent(
        ...     model="gpt-4o",
        ...     temperature=0.2,
        ...     max_tokens=4096
        ... )
    """

    # Create workspace directory if it doesn't exist
    os.makedirs(workspace_dir, exist_ok=True)

    # Determine provider and model
    if model and ":" in model:
        # Format is "provider:model"
        provider_from_model, model_name = model.split(":", 1)
        provider = provider or provider_from_model
        model = model_name

    # Set default provider if not specified
    if not provider:
        provider = "anthropic"  # Default to Anthropic

    # Validate provider
    if provider not in SUPPORTED_PROVIDERS:
        available = ", ".join(SUPPORTED_PROVIDERS.keys())
        raise ValueError(
            f"Unsupported provider: {provider}\n"
            f"Supported providers: {available}\n\n"
            f"Use get_supported_providers() to see all options."
        )

    # Get provider info
    provider_info = SUPPORTED_PROVIDERS[provider]

    # Set default model if not specified
    if not model:
        model = provider_info["default_model"]

    # Set API key in environment if provided
    if api_key and provider_info["env_var"]:
        os.environ[provider_info["env_var"]] = api_key

    # Check if API key is available (unless it's ollama which is local)
    if provider != "ollama" and provider_info["env_var"]:
        if not os.getenv(provider_info["env_var"]):
            raise ValueError(
                f"API key not found for {provider}.\n"
                f"Please set {provider_info['env_var']} environment variable or pass api_key parameter.\n\n"
                f"Example:\n"
                f"  export {provider_info['env_var']}='your-key-here'\n"
                f"  OR\n"
                f"  agent = create_stock_analysis_agent(provider='{provider}', api_key='your-key')"
            )

    try:
        # Create model using LangChain 1.0's unified init_chat_model
        # This automatically handles all provider-specific setup
        chat_model = init_chat_model(
            model=model,
            model_provider=provider,
            temperature=temperature,
            **model_kwargs
        )

        print(f"✓ Initialized {provider} model: {model}")

    except ImportError as e:
        raise ImportError(
            f"Missing package for {provider}.\n"
            f"Please install: pip install {provider_info['package']}\n\n"
            f"Full error: {e}"
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to initialize {provider} model '{model}'.\n"
            f"Error: {e}\n\n"
            f"Available models for {provider}: {', '.join(provider_info['examples'])}"
        )

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
        "model": chat_model  # Use the same model for consistency
    }

    # Create the deep agent with all components
    agent = create_deep_agent(
        model=chat_model,
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


def get_supported_providers() -> Dict[str, Dict[str, Any]]:
    """
    Get information about all supported LLM providers.

    Returns:
        Dictionary mapping provider names to their configuration details

    Example:
        >>> providers = get_supported_providers()
        >>> print(providers["openai"]["default_model"])
        'gpt-4o'
    """
    return SUPPORTED_PROVIDERS.copy()


def list_providers():
    """
    Print a formatted list of all supported LLM providers with examples.

    Example:
        >>> list_providers()
    """
    print("\n" + "="*80)
    print("SUPPORTED LLM PROVIDERS (LangChain 1.0)")
    print("="*80 + "\n")

    for provider, info in SUPPORTED_PROVIDERS.items():
        print(f"📦 {provider}")
        print(f"   Package: {info['package']}")
        print(f"   Default Model: {info['default_model']}")
        if info['env_var']:
            print(f"   API Key: {info['env_var']}")
        print(f"   Examples: {', '.join(info['examples'][:3])}")
        print()

    print("="*80)
    print(f"Total: {len(SUPPORTED_PROVIDERS)} providers supported")
    print("="*80 + "\n")
    print("Usage examples:")
    print('  agent = create_stock_analysis_agent(model="gpt-4o")')
    print('  agent = create_stock_analysis_agent(model="openai:gpt-4o")')
    print('  agent = create_stock_analysis_agent(provider="anthropic", model="claude-sonnet-4-20250514")')
    print()


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

    # Show supported providers
    print("\n🤖 Stock Analysis Deep Agent - LangChain 1.0 Multi-Provider Support\n")

    # Check for any API key
    has_key = any([
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("OPENAI_API_KEY"),
        os.getenv("GOOGLE_API_KEY"),
        os.getenv("COHERE_API_KEY"),
        os.getenv("GROQ_API_KEY"),
        os.getenv("MISTRAL_API_KEY")
    ])

    if not has_key:
        print("⚠️  Warning: No API key found in environment variables.")
        print("\nSupported providers:")
        list_providers()
        print("\nPlease set an API key for your chosen provider:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("  export GOOGLE_API_KEY='your-key-here'")
        print("  ... etc\n")
        sys.exit(1)

    # Create the agent (will use default: Anthropic Claude)
    print("🤖 Creating Stock Analysis Deep Agent...")

    try:
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

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTry listing supported providers:")
        print("  python -c 'from stock_analysis_agent.agent import list_providers; list_providers()'")
        sys.exit(1)
