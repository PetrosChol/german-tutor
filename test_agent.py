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
        from langchain.chat_models import init_chat_model
        print("✓ langchain.chat_models.init_chat_model imported successfully (LangChain 1.0)")
    except ImportError as e:
        print(f"✗ Failed to import init_chat_model: {e}")
        print("  Note: This requires LangChain 1.0+")
        return False

    try:
        sys.path.insert(0, os.path.abspath('.'))
        from stock_analysis_agent import (
            create_stock_analysis_agent,
            run_analysis,
            get_supported_providers,
            list_providers,
            SUPPORTED_PROVIDERS,
            STOCK_TOOLS
        )
        print("✓ stock_analysis_agent package imported successfully")
        print(f"✓ Multi-provider support enabled ({len(SUPPORTED_PROVIDERS)} providers)")
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


def test_providers():
    """Test provider configuration and listing"""
    print("\nTesting provider configuration...")

    try:
        from stock_analysis_agent import get_supported_providers, SUPPORTED_PROVIDERS

        providers = get_supported_providers()
        print(f"✓ Found {len(providers)} supported providers")

        # Verify some key providers
        required_providers = ["openai", "anthropic", "google_genai", "groq", "ollama"]
        for provider in required_providers:
            if provider in providers:
                print(f"  ✓ {provider}: {providers[provider]['default_model']}")
            else:
                print(f"  ✗ Missing provider: {provider}")
                return False

        return True

    except Exception as e:
        print(f"✗ Failed to test providers: {e}")
        return False


def test_agent_structure():
    """Test agent creation with different providers (if API keys available)"""
    print("\nTesting agent creation...")

    # Check if API keys are available
    has_anthropic = os.getenv("ANTHROPIC_API_KEY") is not None
    has_openai = os.getenv("OPENAI_API_KEY") is not None

    if not has_anthropic and not has_openai:
        print("⚠ No API keys found - skipping agent creation test")
        print("  Set ANTHROPIC_API_KEY or OPENAI_API_KEY to test agent creation")
        return True

    try:
        from stock_analysis_agent import create_stock_analysis_agent

        # Test Method 1: Auto-detection (Anthropic)
        if has_anthropic:
            print("  Testing Anthropic with auto-detection...")
            agent = create_stock_analysis_agent(
                model="claude-sonnet-4-20250514",
                workspace_dir="./test_workspace"
            )
            print("  ✓ Anthropic agent created successfully")

        # Test Method 2: Explicit provider (OpenAI)
        if has_openai:
            print("  Testing OpenAI with explicit provider...")
            agent = create_stock_analysis_agent(
                provider="openai",
                model="gpt-4o",
                workspace_dir="./test_workspace"
            )
            print("  ✓ OpenAI agent created successfully")

        # Test Method 3: Provider:model format
        if has_anthropic:
            print("  Testing provider:model format...")
            agent = create_stock_analysis_agent(
                model="anthropic:claude-sonnet-4-20250514",
                workspace_dir="./test_workspace"
            )
            print("  ✓ Provider:model format works")

        print("✓ Agent creation tests passed")
        return True

    except Exception as e:
        print(f"✗ Failed to create agent: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*80)
    print("Stock Analysis Deep Agent - Test Suite (LangChain 1.0)")
    print("="*80 + "\n")

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Tools", test_tools()))
    results.append(("Prompts", test_prompts()))
    results.append(("Provider Configuration", test_providers()))
    results.append(("Agent Creation", test_agent_structure()))

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
        print("\n✨ New in v1.0: Multi-Provider Support (LangChain 1.0)")
        print("  - 14+ LLM providers supported")
        print("  - Unified init_chat_model API")
        print("  - Easy provider switching")
        print("\nNext steps:")
        print("1. Set your API key(s): see .env.example")
        print("2. List providers: python -c 'from stock_analysis_agent import list_providers; list_providers()'")
        print("3. Run examples: python examples/multi_provider_example.py")
        print("4. Or use directly: python stock_analysis_agent/agent.py")
    else:
        print("\n⚠ Some tests failed. Please check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
