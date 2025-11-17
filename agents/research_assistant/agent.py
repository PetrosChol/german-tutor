"""
Research Assistant Deep Agent

A comprehensive research agent for gathering, analyzing, and synthesizing information.
"""

import os
from typing import Optional, List, Any
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import BaseTool

from tools import RESEARCH_TOOLS
from prompts import RESEARCH_ASSISTANT_PROMPT, RESEARCH_SUBAGENT_PROMPT


def create_research_assistant(
    model: str = "claude-sonnet-4-20250514",
    provider: Optional[str] = None,
    temperature: float = 0.1,
    workspace_dir: str = "./research_workspace",
    additional_tools: Optional[List[BaseTool]] = None,
    **model_kwargs
):
    """
    Create a Research Assistant Deep Agent.

    Args:
        model: Model name (e.g., "gpt-4o", "claude-sonnet-4-20250514")
        provider: LLM provider (optional, auto-detected)
        temperature: Model temperature (0.0-1.0)
        workspace_dir: Research workspace directory
        additional_tools: Extra tools beyond defaults
        **model_kwargs: Additional model parameters

    Returns:
        Configured Research Assistant agent

    Examples:
        >>> agent = create_research_assistant()
        >>> agent = create_research_assistant(model="gpt-4o")
        >>> agent = create_research_assistant(
        ...     model="gemini-2.0-flash",
        ...     temperature=0.2
        ... )
    """

    # Create workspace structure
    os.makedirs(f"{workspace_dir}/data/articles", exist_ok=True)
    os.makedirs(f"{workspace_dir}/data/summaries", exist_ok=True)
    os.makedirs(f"{workspace_dir}/data/facts", exist_ok=True)
    os.makedirs(f"{workspace_dir}/reports", exist_ok=True)
    os.makedirs(f"{workspace_dir}/notes", exist_ok=True)

    # Handle provider:model format
    if model and ":" in model:
        provider_from_model, model_name = model.split(":", 1)
        provider = provider or provider_from_model
        model = model_name

    # Set defaults
    if not provider:
        provider = "anthropic"

    # Initialize model
    chat_model = init_chat_model(
        model=model,
        model_provider=provider,
        temperature=temperature,
        **model_kwargs
    )

    print(f"✓ Initialized Research Assistant with {provider}:{model}")

    # Combine tools
    tools = RESEARCH_TOOLS.copy()
    if additional_tools:
        tools.extend(additional_tools)

    # Configure research sub-agent
    research_subagent = {
        "name": "deep_researcher",
        "description": (
            "Use this sub-agent for in-depth research on specific topics. "
            "Ideal for: literature reviews, comparative analysis, gathering "
            "information from multiple sources, processing large volumes of data."
        ),
        "prompt": RESEARCH_SUBAGENT_PROMPT,
        "tools": tools,
        "model": chat_model
    }

    # Create Deep Agent
    agent = create_deep_agent(
        model=chat_model,
        tools=tools,
        system_prompt=RESEARCH_ASSISTANT_PROMPT,
        subagents=[research_subagent],

        filesystem_kwargs={
            "workspace_dir": workspace_dir,
            "description": (
                "Organize your research systematically:\n"
                "- data/articles/ for raw article content\n"
                "- data/summaries/ for summaries\n"
                "- data/facts/ for extracted facts\n"
                "- reports/ for final research reports\n"
                "- notes/ for research notes"
            )
        },

        todolist_kwargs={
            "description": (
                "Plan comprehensive research projects step-by-step. "
                "Break down research into: search, gather, analyze, synthesize, report."
            )
        }
    )

    return agent


def conduct_research(
    topic: str,
    agent: Optional[Any] = None,
    depth: str = "comprehensive",
    save_report: bool = True,
    verbose: bool = True
) -> str:
    """
    Conduct research on a topic.

    Args:
        topic: The research topic or question
        agent: Pre-configured agent (creates new if None)
        depth: Research depth ("quick", "standard", "comprehensive")
        save_report: Whether to save a research report
        verbose: Whether to print results

    Returns:
        Research findings

    Examples:
        >>> conduct_research("AI safety in 2024")
        >>> conduct_research(
        ...     "quantum computing applications",
        ...     depth="comprehensive"
        ... )
    """

    if agent is None:
        agent = create_research_assistant()

    # Construct research prompt based on depth
    depth_prompts = {
        "quick": f"Provide a quick overview of {topic} with 2-3 key sources.",
        "standard": f"Research {topic}. Gather information from 5-7 sources and provide a structured summary.",
        "comprehensive": f"Conduct comprehensive research on {topic}. Gather information from multiple sources, analyze findings, identify trends, and create a detailed report."
    }

    if save_report:
        depth_prompts[depth] += f" Save your findings to reports/{topic.replace(' ', '_')}_research.md"

    query = depth_prompts.get(depth, depth_prompts["standard"])

    # Execute research
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    # Extract response
    messages = result.get("messages", [])
    if messages:
        response = messages[-1].content

        if verbose:
            print("\n" + "="*80)
            print(f"RESEARCH FINDINGS: {topic}")
            print("="*80)
            print(response)
            print("="*80 + "\n")

        return response

    return "No findings generated"


if __name__ == "__main__":
    import sys

    print("\n🔬 Research Assistant Deep Agent\n")

    # Check for API key
    has_key = any([
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("OPENAI_API_KEY"),
        os.getenv("GOOGLE_API_KEY"),
    ])

    if not has_key:
        print("⚠️  No API key found!")
        print("\nSet an API key:")
        print("  export ANTHROPIC_API_KEY='your-key'")
        print("  export OPENAI_API_KEY='your-key'")
        print("  export GOOGLE_API_KEY='your-key'")
        sys.exit(1)

    # Create agent
    print("Creating Research Assistant...")
    agent = create_research_assistant()
    print("✅ Ready to research!\n")

    # Example research tasks
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
        conduct_research(topic, agent=agent)
    else:
        # Interactive mode
        print("Interactive Research Mode")
        print("Enter research topics (Ctrl+C to exit)")
        print("-" * 80)

        try:
            while True:
                topic = input("\n🔍 Research topic: ").strip()
                if not topic:
                    continue

                depth = input("Depth (quick/standard/comprehensive) [standard]: ").strip() or "standard"
                conduct_research(topic, agent=agent, depth=depth)

        except KeyboardInterrupt:
            print("\n\n👋 Research session ended!")
            sys.exit(0)
