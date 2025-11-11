"""
Simple Stock Analysis Example

This example demonstrates basic usage of the Stock Analysis Deep Agent.
"""

import os
import sys

# Add parent directory to path to import stock_analysis_agent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stock_analysis_agent import create_stock_analysis_agent, run_analysis


def main():
    """Run simple stock analysis examples"""

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Error: No API key found!")
        print("\nPlease set your API key:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        print("  OR")
        print("  export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)

    print("="*80)
    print("Stock Analysis Deep Agent - Simple Examples")
    print("="*80 + "\n")

    # Create the agent
    print("🤖 Initializing agent...")
    agent = create_stock_analysis_agent(
        model_provider="anthropic",  # or "openai"
        workspace_dir="./examples/workspace"
    )
    print("✅ Agent ready!\n")

    # Example 1: Simple stock quote
    print("\n" + "="*80)
    print("Example 1: Get Current Stock Quote")
    print("="*80)

    query1 = "What's the current price of Apple (AAPL)?"
    print(f"\nQuery: {query1}\n")
    run_analysis(query1, agent=agent, verbose=True)

    # Example 2: Price change analysis
    print("\n" + "="*80)
    print("Example 2: Analyze Price Changes")
    print("="*80)

    query2 = "How has Microsoft (MSFT) performed over the last 3 months?"
    print(f"\nQuery: {query2}\n")
    run_analysis(query2, agent=agent, verbose=True)

    # Example 3: Stock comparison
    print("\n" + "="*80)
    print("Example 3: Compare Multiple Stocks")
    print("="*80)

    query3 = "Compare Apple and Microsoft stock performance"
    print(f"\nQuery: {query3}\n")
    run_analysis(query3, agent=agent, verbose=True)

    print("\n✅ All examples completed!")
    print("\n📁 Check ./examples/workspace for any saved analysis files")


if __name__ == "__main__":
    main()
