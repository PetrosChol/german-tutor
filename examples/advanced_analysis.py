"""
Advanced Stock Analysis Example

This example demonstrates the Deep Agent capabilities:
- Planning with todo lists
- File system usage for saving reports
- Sub-agent spawning for complex research
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stock_analysis_agent import create_stock_analysis_agent, run_analysis


def main():
    """Run advanced stock analysis examples"""

    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Error: No API key found!")
        print("\nPlease set ANTHROPIC_API_KEY or OPENAI_API_KEY")
        sys.exit(1)

    print("="*80)
    print("Stock Analysis Deep Agent - Advanced Examples")
    print("="*80 + "\n")

    # Create the agent
    print("🤖 Initializing Deep Agent with full capabilities...")
    agent = create_stock_analysis_agent(
        model_provider="anthropic",
        workspace_dir="./examples/advanced_workspace"
    )
    print("✅ Agent ready!\n")

    # Example 1: Comprehensive analysis (demonstrates planning)
    print("\n" + "="*80)
    print("Example 1: Comprehensive Stock Analysis")
    print("="*80)
    print("\nThis will demonstrate the agent's planning capability.")
    print("The agent will break down the analysis into steps using todos.\n")

    query1 = """
    Provide a comprehensive analysis of Tesla (TSLA) including:
    1. Current stock price and today's performance
    2. Price trends over 1 month, 3 months, and 1 year
    3. Recent news and developments
    4. Save your findings to a report file
    """

    print(f"Query: {query1}\n")
    run_analysis(query1, agent=agent, verbose=True)

    # Example 2: Multi-stock comparison (demonstrates file system usage)
    print("\n" + "="*80)
    print("Example 2: Multi-Stock Sector Comparison")
    print("="*80)
    print("\nThis will demonstrate file system usage for organizing data.\n")

    query2 = """
    Compare the top 5 tech stocks: Apple (AAPL), Microsoft (MSFT),
    Google (GOOGL), Amazon (AMZN), and Meta (META).

    For each stock:
    1. Get current price and 1-year performance
    2. Save the comparison to a markdown file called 'tech_giants_comparison.md'
    """

    print(f"Query: {query2}\n")
    run_analysis(query2, agent=agent, verbose=True)

    # Example 3: Deep research (demonstrates sub-agent usage)
    print("\n" + "="*80)
    print("Example 3: Deep Sector Research")
    print("="*80)
    print("\nThis will demonstrate sub-agent spawning for complex research.\n")

    query3 = """
    Conduct a deep analysis of the semiconductor sector.

    Research the major semiconductor companies (NVDA, AMD, INTC, TSM)
    and provide:
    1. Current market positions
    2. Price performance over the past year
    3. Recent news and industry trends
    4. A summary comparison

    Use a sub-agent for the detailed research if needed.
    Save your findings to 'semiconductor_sector_analysis.md'
    """

    print(f"Query: {query3}\n")
    run_analysis(query3, agent=agent, verbose=True)

    print("\n" + "="*80)
    print("✅ All advanced examples completed!")
    print("="*80)
    print("\n📁 Analysis files saved to: ./examples/advanced_workspace")
    print("\nGenerated files:")
    print("  - tesla_analysis.md (or similar)")
    print("  - tech_giants_comparison.md")
    print("  - semiconductor_sector_analysis.md")
    print("\n💡 Tip: Review these files to see how the agent organized its work!")


if __name__ == "__main__":
    main()
