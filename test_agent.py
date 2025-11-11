"""
Test script to verify the Stock Analysis Deep Agent setup.

This script tests:
1. Package imports
2. Agent creation
3. Tool availability
4. Basic structure validation
"""

import sys
import os

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")

    try:
        import deepagents
        print("✓ deepagents imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import deepagents: {e}")
        return False

    try:
        from langchain_anthropic import ChatAnthropic
        print("✓ langchain_anthropic imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import langchain_anthropic: {e}")
        return False

    try:
        from langchain_openai import ChatOpenAI
        print("✓ langchain_openai imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import langchain_openai: {e}")
        return False

    try:
        sys.path.insert(0, os.path.abspath('.'))
        from stock_analysis_agent import create_stock_analysis_agent, run_analysis, STOCK_TOOLS
        print("✓ stock_analysis_agent package imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import stock_analysis_agent: {e}")
        return False

    return True


def test_tools():
    """Test that all tools are available"""
    print("\nTesting tools...")

    try:
        from stock_analysis_agent import STOCK_TOOLS
        print(f"✓ Found {len(STOCK_TOOLS)} stock analysis tools:")
        for tool in STOCK_TOOLS:
            print(f"  - {tool.name}: {tool.description[:60]}...")
        return True
    except Exception as e:
        print(f"✗ Failed to load tools: {e}")
        return False


def test_prompts():
    """Test that prompts are properly configured"""
    print("\nTesting prompts...")

    try:
        from stock_analysis_agent import STOCK_ANALYST_PROMPT, RESEARCH_SUBAGENT_PROMPT
        print(f"✓ Main prompt loaded ({len(STOCK_ANALYST_PROMPT)} characters)")
        print(f"✓ Research sub-agent prompt loaded ({len(RESEARCH_SUBAGENT_PROMPT)} characters)")
        return True
    except Exception as e:
        print(f"✗ Failed to load prompts: {e}")
        return False


def test_agent_structure():
    """Test agent creation without API key (structure only)"""
    print("\nTesting agent structure...")

    # Check if API keys are available
    has_anthropic = os.getenv("ANTHROPIC_API_KEY") is not None
    has_openai = os.getenv("OPENAI_API_KEY") is not None

    if not has_anthropic and not has_openai:
        print("⚠ No API keys found - skipping agent creation test")
        print("  Set ANTHROPIC_API_KEY or OPENAI_API_KEY to test agent creation")
        return True

    try:
        from stock_analysis_agent import create_stock_analysis_agent

        provider = "anthropic" if has_anthropic else "openai"
        print(f"  Creating agent with {provider}...")

        agent = create_stock_analysis_agent(
            model_provider=provider,
            workspace_dir="./test_workspace"
        )

        print("✓ Agent created successfully")
        print(f"  Type: {type(agent)}")
        return True

    except Exception as e:
        print(f"✗ Failed to create agent: {e}")
        return False


def main():
    """Run all tests"""
    print("="*80)
    print("Stock Analysis Deep Agent - Test Suite")
    print("="*80 + "\n")

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Tools", test_tools()))
    results.append(("Prompts", test_prompts()))
    results.append(("Agent Structure", test_agent_structure()))

    # Print summary
    print("\n" + "="*80)
    print("Test Summary")
    print("="*80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:.<40} {status}")

    print("="*80)
    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The Stock Analysis Deep Agent is ready to use.")
        print("\nNext steps:")
        print("1. Set your API key: export ANTHROPIC_API_KEY='your-key'")
        print("2. Run examples: python examples/simple_analysis.py")
        print("3. Or use directly: python stock_analysis_agent/agent.py")
    else:
        print("\n⚠ Some tests failed. Please check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
