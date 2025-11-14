"""
Multi-Provider Example - LangChain 1.0

This example demonstrates how to use the Stock Analysis Deep Agent with
different LLM providers using LangChain 1.0's unified init_chat_model API.

Supported providers:
- OpenAI (GPT-4, GPT-3.5, etc.)
- Anthropic (Claude)
- Google (Gemini via Vertex AI or direct API)
- Cohere
- Groq (fast inference)
- Together AI
- Mistral AI
- Fireworks AI
- Ollama (local models)
- AWS Bedrock
- Azure OpenAI
- DeepSeek
- xAI (Grok)
- Perplexity AI
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stock_analysis_agent import create_stock_analysis_agent, run_analysis, list_providers


def example_openai():
    """Example using OpenAI GPT-4"""
    print("\n" + "="*80)
    print("Example 1: OpenAI GPT-4o")
    print("="*80 + "\n")

    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Skipping: OPENAI_API_KEY not set")
        return

    # Method 1: Auto-detection (model name starts with "gpt")
    agent = create_stock_analysis_agent(model="gpt-4o")

    # Method 2: Explicit provider
    # agent = create_stock_analysis_agent(provider="openai", model="gpt-4o")

    # Method 3: Provider:model format
    # agent = create_stock_analysis_agent(model="openai:gpt-4o")

    query = "What's the current price of Microsoft stock?"
    run_analysis(query, agent=agent)


def example_anthropic():
    """Example using Anthropic Claude"""
    print("\n" + "="*80)
    print("Example 2: Anthropic Claude Sonnet 4")
    print("="*80 + "\n")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Skipping: ANTHROPIC_API_KEY not set")
        return

    # Method 1: Auto-detection (model name starts with "claude")
    agent = create_stock_analysis_agent(model="claude-sonnet-4-20250514")

    # Method 2: Explicit provider
    # agent = create_stock_analysis_agent(
    #     provider="anthropic",
    #     model="claude-sonnet-4-20250514"
    # )

    query = "What's Tesla's current stock price?"
    run_analysis(query, agent=agent)


def example_google_genai():
    """Example using Google Gemini (direct API)"""
    print("\n" + "="*80)
    print("Example 3: Google Gemini 2.0 Flash")
    print("="*80 + "\n")

    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Skipping: GOOGLE_API_KEY not set")
        print("   To use Google Gemini, set GOOGLE_API_KEY")
        print("   Get one at: https://makersuite.google.com/app/apikey")
        return

    # Requires: pip install langchain-google-genai
    agent = create_stock_analysis_agent(
        provider="google_genai",
        model="gemini-2.0-flash"
    )

    # Or with provider:model format
    # agent = create_stock_analysis_agent(model="google_genai:gemini-2.0-flash")

    query = "What's the price of Apple stock?"
    run_analysis(query, agent=agent)


def example_groq():
    """Example using Groq (fast inference)"""
    print("\n" + "="*80)
    print("Example 4: Groq (Llama 3.3 70B)")
    print("="*80 + "\n")

    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  Skipping: GROQ_API_KEY not set")
        print("   To use Groq, set GROQ_API_KEY")
        print("   Get one at: https://console.groq.com/keys")
        return

    # Requires: pip install langchain-groq
    agent = create_stock_analysis_agent(
        provider="groq",
        model="llama-3.3-70b-versatile"
    )

    query = "What's Amazon's current stock price?"
    run_analysis(query, agent=agent)


def example_ollama():
    """Example using Ollama (local models)"""
    print("\n" + "="*80)
    print("Example 5: Ollama (Local Llama 3.2)")
    print("="*80 + "\n")

    print("ℹ️  Note: This requires Ollama to be running locally")
    print("   Install: https://ollama.ai")
    print("   Pull model: ollama pull llama3.2")
    print()

    try:
        # Requires: pip install langchain-ollama
        # No API key needed for Ollama
        agent = create_stock_analysis_agent(
            provider="ollama",
            model="llama3.2"
        )

        query = "What's the current price of NVIDIA stock?"
        run_analysis(query, agent=agent)

    except Exception as e:
        print(f"⚠️  Error: {e}")
        print("   Make sure Ollama is installed and running")


def example_cohere():
    """Example using Cohere"""
    print("\n" + "="*80)
    print("Example 6: Cohere Command R+")
    print("="*80 + "\n")

    if not os.getenv("COHERE_API_KEY"):
        print("⚠️  Skipping: COHERE_API_KEY not set")
        print("   To use Cohere, set COHERE_API_KEY")
        print("   Get one at: https://dashboard.cohere.com/api-keys")
        return

    # Requires: pip install langchain-cohere
    agent = create_stock_analysis_agent(
        model="command-r-plus",  # Auto-detects "command" -> cohere
        temperature=0.1
    )

    query = "What's Google's stock price?"
    run_analysis(query, agent=agent)


def example_mistralai():
    """Example using Mistral AI"""
    print("\n" + "="*80)
    print("Example 7: Mistral Large")
    print("="*80 + "\n")

    if not os.getenv("MISTRAL_API_KEY"):
        print("⚠️  Skipping: MISTRAL_API_KEY not set")
        print("   To use Mistral, set MISTRAL_API_KEY")
        print("   Get one at: https://console.mistral.ai/")
        return

    # Requires: pip install langchain-mistralai
    agent = create_stock_analysis_agent(
        model="mistral-large-latest",  # Auto-detects "mistral" -> mistralai
    )

    query = "What's Meta's current stock price?"
    run_analysis(query, agent=agent)


def example_with_custom_params():
    """Example with custom model parameters"""
    print("\n" + "="*80)
    print("Example 8: Custom Parameters (Higher Temperature)")
    print("="*80 + "\n")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Skipping: ANTHROPIC_API_KEY not set")
        return

    # You can pass additional parameters to the model
    agent = create_stock_analysis_agent(
        model="claude-sonnet-4-20250514",
        temperature=0.5,  # Higher temperature for more creative responses
        max_tokens=4096   # Limit response length
    )

    query = "What's the current price of Netflix stock?"
    run_analysis(query, agent=agent)


def main():
    """Run multi-provider examples"""

    print("="*80)
    print("Stock Analysis Deep Agent - Multi-Provider Examples (LangChain 1.0)")
    print("="*80)

    # Show all supported providers
    print("\n📋 Listing all supported providers...\n")
    list_providers()

    print("\n" + "="*80)
    print("Running Examples")
    print("="*80)
    print("\nNote: Examples will be skipped if API keys are not set.")
    print("Set environment variables for the providers you want to test.\n")

    # Run examples
    examples = [
        ("OpenAI", example_openai),
        ("Anthropic", example_anthropic),
        ("Google Gemini", example_google_genai),
        ("Groq", example_groq),
        ("Ollama", example_ollama),
        ("Cohere", example_cohere),
        ("Mistral AI", example_mistralai),
        ("Custom Parameters", example_with_custom_params)
    ]

    for name, example_func in examples:
        try:
            example_func()
        except ImportError as e:
            print(f"\n⚠️  {name} example skipped: {e}")
            print(f"   Install the required package to use this provider")
        except Exception as e:
            print(f"\n❌ {name} example failed: {e}")

    print("\n" + "="*80)
    print("✅ Multi-Provider Examples Complete")
    print("="*80)
    print("\nKey Takeaways:")
    print("1. LangChain 1.0's init_chat_model provides a unified interface")
    print("2. You can use provider:model format OR specify provider separately")
    print("3. LangChain auto-detects many providers from model names")
    print("4. Just install the provider package you need (e.g., pip install langchain-groq)")
    print("5. All providers work with the same Deep Agent architecture")
    print()


if __name__ == "__main__":
    main()
