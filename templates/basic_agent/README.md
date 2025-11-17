# Deep Agent Template - Basic

This template provides a starting point for building your own Deep Agent using the Deep Agents framework and LangChain 1.0.

## Quick Start

### 1. Copy this template

```bash
cp -r templates/basic_agent my_agent
cd my_agent
```

### 2. Install dependencies

```bash
pip install deepagents langgraph langchain>=1.0.0 langchain-core>=1.0.0

# Install your chosen LLM provider
pip install langchain-anthropic  # For Claude
# OR
pip install langchain-openai     # For GPT-4
# OR
pip install langchain-google-genai  # For Gemini
```

### 3. Set your API key

```bash
export ANTHROPIC_API_KEY='your-key-here'
# OR
export OPENAI_API_KEY='your-key-here'
# OR
export GOOGLE_API_KEY='your-key-here'
```

### 4. Customize for your domain

1. **Edit `tools.py`**: Replace example tools with your domain-specific tools
2. **Edit `prompts.py`**: Customize the system prompt for your use case
3. **Edit `agent.py`**: Adjust configuration as needed

### 5. Run your agent

```bash
# Interactive mode
python agent.py

# Single command
python agent.py "Your task here"

# Programmatic usage
python
>>> from agent import create_agent, run_task
>>> agent = create_agent()
>>> run_task("Your task", agent)
```

## File Structure

```
basic_agent/
├── __init__.py        # Package initialization
├── agent.py           # Main agent creation and execution
├── tools.py           # Custom tools for your domain
├── prompts.py         # System prompts
├── README.md          # This file
└── requirements.txt   # Dependencies (create this)
```

## Customization Guide

### Adding Tools

In `tools.py`:

```python
@tool
def my_custom_tool(param: str) -> str:
    """
    Description of what this tool does.

    Args:
        param: Description

    Returns:
        JSON string with results
    """
    try:
        # Your logic here
        result = do_something(param)
        return json.dumps({"success": True, "data": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

# Add to TOOLS list
TOOLS = [
    example_tool_1,
    example_tool_2,
    my_custom_tool,  # Add your tool
]
```

### Customizing the Prompt

In `prompts.py`:

1. Replace `[YOUR_DOMAIN]` with your domain (e.g., "legal", "medical", "financial")
2. Replace `[ROLE_DESCRIPTION]` with the specific role
3. Update tool descriptions
4. Add domain-specific examples
5. Add domain-specific best practices

### Using Different LLM Providers

```python
# Anthropic Claude (default)
agent = create_agent()

# OpenAI GPT-4
agent = create_agent(model="gpt-4o")

# Google Gemini
agent = create_agent(provider="google_genai", model="gemini-2.0-flash")

# Groq (fast, cheap)
agent = create_agent(provider="groq", model="llama-3.3-70b-versatile")

# Local with Ollama
agent = create_agent(provider="ollama", model="llama3.2")
```

### Enabling Sub-agents

For complex tasks that benefit from delegation:

```python
agent = create_agent(enable_subagents=True)
```

Then in your system prompt, guide the agent on when to use sub-agents.

## Examples

### Example 1: Simple Query

```python
from agent import create_agent, run_task

agent = create_agent()
response = run_task("Simple question here", agent)
```

### Example 2: Complex Task

```python
agent = create_agent()
response = run_task(
    "Perform comprehensive analysis of X including Y and Z, "
    "save findings to a report",
    agent
)
```

### Example 3: Different Provider

```python
# Use Google Gemini for cost savings
agent = create_agent(
    provider="google_genai",
    model="gemini-2.0-flash",
    temperature=0.2
)

response = run_task("Your task", agent)
```

## Testing Your Agent

Create a test file:

```python
# test_agent.py
from agent import create_agent, run_task

def test_simple():
    agent = create_agent()
    response = run_task("Test query", agent, verbose=False)
    assert response is not None
    assert len(response) > 0
    print("✓ Simple test passed")

def test_complex():
    agent = create_agent()
    response = run_task(
        "Complex multi-step task",
        agent,
        verbose=False
    )
    assert response is not None
    print("✓ Complex test passed")

if __name__ == "__main__":
    test_simple()
    test_complex()
    print("\nAll tests passed!")
```

## Best Practices

1. **Tool Design**
   - Keep tools focused (one purpose each)
   - Return JSON for structured data
   - Handle errors gracefully
   - Document with examples

2. **Prompt Engineering**
   - Be specific about when to plan
   - Provide clear examples
   - Structure with headings
   - Include domain expertise

3. **File System Usage**
   - Save large outputs
   - Organize with subdirectories
   - Use descriptive filenames
   - Clean up old files periodically

4. **Testing**
   - Test with multiple providers
   - Test simple and complex tasks
   - Test error handling
   - Monitor costs and performance

## Troubleshooting

**Agent doesn't plan when it should:**
- Make planning more explicit in the prompt
- Add "MUST use write_todos" for multi-step tasks

**Too many small files:**
- Add guidance about minimum file size (>100 words)

**Context overflow:**
- Enforce file system usage for large outputs
- Use sub-agents for context isolation

**Costs too high:**
- Use cheaper models (Gemini, Groq)
- Use GPT-4o-mini for sub-agents
- Limit max_tokens

## Next Steps

1. Replace example tools with your domain tools
2. Customize the system prompt
3. Test thoroughly
4. Deploy to production
5. Monitor and iterate

## Resources

- [Deep Agents Guide](../../docs/DEEP_AGENTS_GUIDE.md)
- [LangChain Docs](https://python.langchain.com/)
- [Deep Agents GitHub](https://github.com/langchain-ai/deepagents)

Happy building! 🚀
