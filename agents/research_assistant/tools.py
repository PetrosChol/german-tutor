"""
Research Assistant Tools

Tools for gathering, analyzing, and synthesizing research information.
"""

import json
import requests
from typing import Optional, List
from langchain_core.tools import tool
from bs4 import BeautifulSoup


@tool
def web_search(
    query: str,
    num_results: int = 5
) -> str:
    """
    Search the web for information on a topic.

    Use this when you need to find current information, articles, or data
    about a topic from the internet.

    Args:
        query: The search query
        num_results: Number of results to return (default: 5)

    Returns:
        JSON string with search results including titles, snippets, and URLs

    Example:
        web_search("artificial intelligence recent developments", 3)
    """
    try:
        # In a real implementation, you'd use a search API (Google, Bing, DuckDuckGo)
        # This is a simplified example
        results = {
            "query": query,
            "results": [
                {
                    "title": f"Result {i+1} for {query}",
                    "snippet": f"Information about {query}...",
                    "url": f"https://example.com/result{i+1}"
                }
                for i in range(num_results)
            ],
            "count": num_results
        }

        return json.dumps(results, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "query": query
        })


@tool
def fetch_article_content(url: str) -> str:
    """
    Fetch and extract the main content from a web article.

    Use this to get the full text of articles, papers, or web pages
    that you found through web_search.

    Args:
        url: The URL of the article to fetch

    Returns:
        JSON string with article content

    Example:
        fetch_article_content("https://example.com/article")
    """
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Research Assistant Bot)'
        })

        if response.status_code != 200:
            return json.dumps({
                "success": False,
                "error": f"HTTP {response.status_code}",
                "url": url
            })

        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text (simplified - in reality you'd want more sophisticated extraction)
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return json.dumps({
            "success": True,
            "url": url,
            "content": text[:5000],  # Limit to first 5000 chars
            "length": len(text),
            "truncated": len(text) > 5000
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "url": url
        })


@tool
def summarize_text(
    text: str,
    max_length: int = 200
) -> str:
    """
    Create a concise summary of a longer text.

    Use this to condense long articles or documents into key points.

    Args:
        text: The text to summarize
        max_length: Maximum length of summary in words (default: 200)

    Returns:
        JSON string with summary

    Example:
        summarize_text("Long article text here...", 100)
    """
    try:
        # Simple summarization (in production, use a proper summarization model)
        words = text.split()

        if len(words) <= max_length:
            summary = text
        else:
            # Take first and last portions
            start = " ".join(words[:max_length//2])
            end = " ".join(words[-max_length//2:])
            summary = f"{start}...\n\n{end}"

        return json.dumps({
            "success": True,
            "original_length": len(words),
            "summary_length": len(summary.split()),
            "summary": summary
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@tool
def extract_key_facts(text: str, num_facts: int = 5) -> str:
    """
    Extract key facts and important information from text.

    Use this to identify the most important pieces of information
    from research materials.

    Args:
        text: The text to analyze
        num_facts: Number of key facts to extract (default: 5)

    Returns:
        JSON string with extracted facts

    Example:
        extract_key_facts("Research paper content...", 3)
    """
    try:
        # Simple fact extraction (in production, use NLP models)
        # This is a placeholder - extract sentences with keywords
        sentences = text.split('. ')
        keywords = ['important', 'key', 'significant', 'found', 'discovered',
                   'showed', 'demonstrated', 'concluded', 'evidence', 'result']

        facts = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                facts.append(sentence.strip())
            if len(facts) >= num_facts:
                break

        return json.dumps({
            "success": True,
            "facts": facts[:num_facts],
            "count": len(facts)
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@tool
def compare_sources(
    source1_text: str,
    source2_text: str
) -> str:
    """
    Compare information from two different sources.

    Use this to identify agreements, contradictions, and unique
    information across sources.

    Args:
        source1_text: Text from first source
        source2_text: Text from second source

    Returns:
        JSON string with comparison results

    Example:
        compare_sources("Source 1 text...", "Source 2 text...")
    """
    try:
        # Simple comparison (in production, use semantic similarity)
        words1 = set(source1_text.lower().split())
        words2 = set(source2_text.lower().split())

        common = words1 & words2
        unique1 = words1 - words2
        unique2 = words2 - words1

        return json.dumps({
            "success": True,
            "common_terms_count": len(common),
            "unique_to_source1": len(unique1),
            "unique_to_source2": len(unique2),
            "similarity_score": len(common) / max(len(words1), len(words2)),
            "common_sample": list(common)[:10]
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


# Export all tools
RESEARCH_TOOLS = [
    web_search,
    fetch_article_content,
    summarize_text,
    extract_key_facts,
    compare_sources
]
