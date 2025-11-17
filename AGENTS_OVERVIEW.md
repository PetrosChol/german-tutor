# Deep Agents Implementation - Complete Overview

This repository now contains comprehensive resources for building effective AI agents using Deep Agents + LangChain 1.0.

## 📚 What's Included

### 1. Comprehensive Guide
**Location**: `docs/DEEP_AGENTS_GUIDE.md`

A 100+ page definitive guide covering:
- ✅ Introduction to Deep Agents (what, why, benefits)
- ✅ Core Concepts (4 pillars: Planning, File System, Sub-agents, Prompts)
- ✅ Architecture Overview (components, middleware, file structure)
- ✅ Step-by-Step Guide (8 detailed steps from concept to deployment)
- ✅ Best Practices (planning, file system, sub-agents, error handling)
- ✅ Advanced Patterns (parallel agents, iterative refinement, collaboration)
- ✅ Troubleshooting (common issues and solutions)
- ✅ Production Deployment (checklist, monitoring, cost control, security)
- ✅ Quick Reference Card

### 2. Reusable Templates
**Location**: `templates/basic_agent/`

A complete agent template ready to customize:
- `tools.py` - Example tools with best practices
- `prompts.py` - Structured system prompt template
- `agent.py` - Full agent implementation with multi-provider support
- `README.md` - Detailed customization guide
- `__init__.py` - Package structure

**Features**:
- Multi-provider support (15+ LLMs)
- TodoListMiddleware integration
- FilesystemMiddleware integration
- SubAgentMiddleware support
- Interactive and programmatic modes
- Comprehensive error handling

### 3. Three Production-Ready Agents

#### Agent 1: Research Assistant
**Location**: `agents/research_assistant/`

**Purpose**: Comprehensive research, literature reviews, information synthesis

**Tools**:
- `web_search()` - Search the web
- `fetch_article_content()` - Retrieve full articles
- `summarize_text()` - Create summaries
- `extract_key_facts()` - Identify key information
- `compare_sources()` - Compare multiple sources

**Capabilities**:
- Systematic research planning
- Multi-source information gathering
- Critical analysis and synthesis
- Structured report generation
- Source citation and verification

**Usage**:
```python
from agents.research_assistant import create_research_assistant, conduct_research

agent = create_research_assistant()
conduct_research("AI safety in 2024", agent, depth="comprehensive")
```

**Use Cases**:
- Literature reviews
- Competitive analysis
- Market research
- Academic research
- Fact-checking
- Background research

#### Agent 2: Code Review Agent
**Location**: `agents/code_reviewer/` (to be implemented)

**Purpose**: Automated code review, security analysis, best practices

**Planned Tools**:
- `analyze_code_quality()` - Check code quality metrics
- `find_security_issues()` - Identify security vulnerabilities
- `suggest_improvements()` - Recommend code improvements
- `check_style()` - Verify code style compliance
- `detect_bugs()` - Find potential bugs

**Planned Capabilities**:
- Multi-language support
- Security vulnerability detection
- Performance analysis
- Best practice recommendations
- Automated documentation suggestions

#### Agent 3: Content Writer Agent
**Location**: `agents/content_writer/` (to be implemented)

**Purpose**: Professional content creation, editing, optimization

**Planned Tools**:
- `generate_outline()` - Create content outlines
- `write_section()` - Write content sections
- `improve_readability()` - Enhance readability
- `check_seo()` - SEO optimization
- `fact_check()` - Verify factual accuracy

**Planned Capabilities**:
- Multi-format content (blogs, articles, documentation)
- SEO optimization
- Tone and style adaptation
- Fact-checking integration
- Plagiarism detection

### 4. Stock Analysis Agent (Already Implemented)
**Location**: `stock_analysis_agent/`

**Purpose**: Stock market analysis with Deep Agents

**Features**:
- Real-time stock data
- Historical analysis
- News integration
- Multi-stock comparison
- Report generation

## 🎯 Key Features Across All Agents

### Multi-Provider Support (LangChain 1.0)
All agents support 15+ LLM providers:
- Anthropic (Claude Sonnet 4, Claude Opus 4)
- OpenAI (GPT-4o, GPT-4 Turbo)
- Google (Gemini 2.0 Flash, Gemini 1.5 Pro)
- Groq (Llama 3.3, Mixtral)
- Cohere, Mistral, Fireworks, Together AI
- Ollama (local models - free!)
- AWS Bedrock, Azure OpenAI, DeepSeek, xAI, Perplexity

### Deep Agent Capabilities
All agents implement the 4 pillars:

1. **Planning (TodoListMiddleware)**
   - Automatic task breakdown
   - Progress tracking
   - Dynamic plan adaptation

2. **File System (FilesystemMiddleware)**
   - Organized workspace structure
   - Context preservation
   - Report generation

3. **Sub-agents (SubAgentMiddleware)**
   - Parallel processing
   - Specialized delegation
   - Context isolation

4. **Expert Prompts**
   - Domain-specific guidance
   - Detailed examples
   - Best practices built-in

## 📖 Quick Start

### For Learning

1. **Read the Guide**:
   ```bash
   cat docs/DEEP_AGENTS_GUIDE.md
   ```

2. **Try the Stock Analysis Agent**:
   ```bash
   export ANTHROPIC_API_KEY='your-key'
   python stock_analysis_agent/agent.py
   ```

3. **Try the Research Assistant**:
   ```bash
   python agents/research_assistant/agent.py "AI trends 2024"
   ```

### For Building Your Own Agent

1. **Copy the Template**:
   ```bash
   cp -r templates/basic_agent my_custom_agent
   cd my_custom_agent
   ```

2. **Customize**:
   - Edit `tools.py` with your domain tools
   - Edit `prompts.py` with your system prompt
   - Adjust `agent.py` as needed

3. **Run**:
   ```bash
   python agent.py "Your task"
   ```

### For Using Existing Agents

```python
# Research Assistant
from agents.research_assistant import create_research_assistant, conduct_research
agent = create_research_assistant()
conduct_research("your topic", agent)

# Stock Analysis
from stock_analysis_agent import create_stock_analysis_agent, run_analysis
agent = create_stock_analysis_agent()
run_analysis("analyze AAPL", agent)
```

## 🛠️ Installation

### Core Dependencies
```bash
pip install deepagents langgraph langchain>=1.0.0 langchain-core>=1.0.0
```

### LLM Providers (choose one or more)
```bash
pip install langchain-anthropic     # For Claude
pip install langchain-openai        # For GPT-4
pip install langchain-google-genai  # For Gemini
pip install langchain-groq          # For Groq
pip install langchain-ollama        # For local models
# ... etc
```

### Agent-Specific Dependencies
```bash
# For Research Assistant
pip install requests beautifulsoup4

# For Stock Analysis
pip install requests beautifulsoup4

# For Code Reviewer (when implemented)
pip install ast-grep radon pylint

# For Content Writer (when implemented)
pip install nltk textstat
```

## 📊 Comparison of Agents

| Agent | Domain | Complexity | Best Provider | Use Cases |
|-------|--------|------------|---------------|-----------|
| **Stock Analysis** | Finance | Medium | Claude/GPT-4 | Market research, stock analysis |
| **Research Assistant** | General | High | Claude Sonnet 4 | Literature reviews, research |
| **Code Reviewer** | Software | High | GPT-4/Claude | Code quality, security |
| **Content Writer** | Marketing | Medium | GPT-4/Gemini | Blogs, articles, SEO |

## 🎓 Learning Path

1. **Beginner**: Start with the Stock Analysis Agent
   - Simpler domain
   - Clear use cases
   - Good examples

2. **Intermediate**: Use the Research Assistant
   - More complex workflows
   - Multi-step planning
   - File system usage

3. **Advanced**: Build custom agents
   - Use the template
   - Implement domain tools
   - Custom prompts

4. **Expert**: Multi-agent systems
   - Chain agents together
   - Parallel processing
   - Production deployment

## 📈 Architecture Patterns

### Pattern 1: Single Agent
```
User → Agent → Tools → Response
```
Best for: Simple, focused tasks

### Pattern 2: Agent + Sub-agents
```
User → Main Agent → Sub-agent 1 (specialized)
                  → Sub-agent 2 (specialized)
                  → Synthesis → Response
```
Best for: Complex, multi-faceted tasks

### Pattern 3: Agent Chain
```
User → Agent A → File → Agent B → File → Agent C → Response
```
Best for: Multi-stage processing

### Pattern 4: Parallel Agents
```
User → Dispatcher → Agent A (parallel)
                 → Agent B (parallel)
                 → Agent C (parallel)
                 → Aggregator → Response
```
Best for: Independent parallel tasks

## 🔧 Customization Guide

### Adding New Tools
```python
# In tools.py
@tool
def your_tool(param: str) -> str:
    """Tool description"""
    try:
        result = your_logic(param)
        return json.dumps({"success": True, "data": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
```

### Modifying System Prompts
```python
# In prompts.py
YOUR_PROMPT = """
You are [ROLE].

# Capabilities
[Tools]

# Approach
[Guidance]

# Examples
[Examples]
"""
```

### Changing LLM Providers
```python
# Any agent
agent = create_agent(
    model="gpt-4o",              # or "gemini-2.0-flash"
    provider="openai",           # or "google_genai"
    temperature=0.1
)
```

## 🧪 Testing

Each agent includes tests:
```bash
# Research Assistant
python agents/research_assistant/agent.py "test topic"

# Stock Analysis
python test_agent.py

# Your custom agent
python my_agent/agent.py "test task"
```

## 🚀 Production Deployment

See `docs/DEEP_AGENTS_GUIDE.md` Section 8 for:
- Deployment checklist
- Monitoring setup
- Cost control
- Security hardening
- Load testing
- Error handling

## 📝 Documentation Structure

```
docs/
└── DEEP_AGENTS_GUIDE.md       # Complete 100+ page guide

templates/
└── basic_agent/               # Reusable template
    ├── README.md
    ├── agent.py
    ├── tools.py
    └── prompts.py

agents/
├── research_assistant/        # Production agent
├── code_reviewer/            # Coming soon
└── content_writer/           # Coming soon

stock_analysis_agent/          # Stock analysis (implemented)

examples/
├── simple_analysis.py
├── advanced_analysis.py
└── multi_provider_example.py
```

## 🎯 Next Steps

1. ✅ **Completed**:
   - Comprehensive guide
   - Template system
   - Research Assistant agent
   - Stock Analysis agent
   - Multi-provider support

2. 🚧 **In Progress**:
   - Code Review agent
   - Content Writer agent
   - Example scripts

3. 📋 **Planned**:
   - More agent examples
   - Video tutorials
   - Deployment guides
   - Community agents

## 💡 Best Practices Summary

1. **Planning**: Use write_todos for 3+ step tasks
2. **Files**: Save outputs >500 words
3. **Sub-agents**: Delegate specialized research
4. **Prompts**: Include detailed examples
5. **Tools**: Return JSON, handle errors
6. **Testing**: Test with multiple providers
7. **Monitoring**: Log usage and costs

## 🤝 Contributing

Areas for contribution:
- Additional agent templates
- New domain-specific agents
- Tool improvements
- Documentation enhancements
- Bug fixes and optimizations

## 📚 Resources

- **Deep Agents Blog**: https://blog.langchain.com/deep-agents/
- **LangChain 1.0 Docs**: https://python.langchain.com/
- **Deep Agents GitHub**: https://github.com/langchain-ai/deepagents
- **This Guide**: `docs/DEEP_AGENTS_GUIDE.md`

---

**Built with Deep Agents + LangChain 1.0**

*Empowering developers to build truly intelligent, long-horizon AI agents*
