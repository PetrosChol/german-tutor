"""
Stock analysis tools for the Deep Agents framework.
These tools provide stock data fetching, news search, and analysis capabilities.
"""

import json
import requests
from typing import Optional, Dict, Any
from langchain_core.tools import tool


@tool
def get_stock_quote(ticker: str) -> str:
    """
    Fetch current stock price and basic quote information for a given ticker symbol.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')

    Returns:
        JSON string with stock quote data including price, volume, and market cap.

    Example:
        get_stock_quote("AAPL") -> Returns current Apple stock information
    """
    try:
        # Using a free API endpoint (finnhub.io alternative - using a mock response for demo)
        # In production, you'd use a real API like Alpha Vantage, Finnhub, or Yahoo Finance

        # For demonstration, we'll use a simple web scraping approach
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "range": "1d"
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            # Extract relevant information
            chart_data = data.get("chart", {}).get("result", [{}])[0]
            meta = chart_data.get("meta", {})

            result = {
                "ticker": ticker.upper(),
                "current_price": meta.get("regularMarketPrice"),
                "previous_close": meta.get("previousClose"),
                "day_high": meta.get("regularMarketDayHigh"),
                "day_low": meta.get("regularMarketDayLow"),
                "volume": meta.get("regularMarketVolume"),
                "currency": meta.get("currency"),
                "exchange": meta.get("exchangeName"),
                "timestamp": meta.get("regularMarketTime")
            }

            return json.dumps(result, indent=2)
        else:
            return json.dumps({
                "error": f"Failed to fetch data for {ticker}",
                "status_code": response.status_code
            })

    except Exception as e:
        return json.dumps({
            "error": f"Error fetching stock quote: {str(e)}",
            "ticker": ticker
        })


@tool
def search_stock_news(ticker: str, num_results: int = 5) -> str:
    """
    Search for recent news articles about a specific stock or company.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        num_results: Number of news articles to return (default: 5)

    Returns:
        JSON string with news articles including titles, descriptions, and URLs.

    Example:
        search_stock_news("TSLA", 3) -> Returns 3 recent Tesla news articles
    """
    try:
        # In production, you'd use a news API like NewsAPI, Finnhub, or Alpha Vantage
        # For demonstration, we'll return a structured response

        # Using Yahoo Finance news feed
        url = f"https://query1.finance.yahoo.com/v1/finance/search"
        params = {
            "q": ticker,
            "quotesCount": 0,
            "newsCount": num_results,
            "enableFuzzyQuery": False
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            news_items = data.get("news", [])

            articles = []
            for item in news_items[:num_results]:
                articles.append({
                    "title": item.get("title"),
                    "publisher": item.get("publisher"),
                    "link": item.get("link"),
                    "published_at": item.get("providerPublishTime")
                })

            return json.dumps({
                "ticker": ticker.upper(),
                "articles": articles,
                "count": len(articles)
            }, indent=2)
        else:
            return json.dumps({
                "error": f"Failed to fetch news for {ticker}",
                "status_code": response.status_code
            })

    except Exception as e:
        return json.dumps({
            "error": f"Error searching news: {str(e)}",
            "ticker": ticker
        })


@tool
def calculate_price_change(ticker: str, period: str = "1mo") -> str:
    """
    Calculate price change and percentage change for a stock over a specified period.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        period: Time period for comparison. Options: '1d', '5d', '1mo', '3mo', '6mo', '1y'

    Returns:
        JSON string with price change data and percentage change.

    Example:
        calculate_price_change("AAPL", "1mo") -> Returns Apple's price change over 1 month
    """
    try:
        # Map period to Yahoo Finance API range
        period_map = {
            "1d": "1d",
            "5d": "5d",
            "1mo": "1mo",
            "3mo": "3mo",
            "6mo": "6mo",
            "1y": "1y"
        }

        range_param = period_map.get(period, "1mo")

        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "range": range_param
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            chart_data = data.get("chart", {}).get("result", [{}])[0]

            # Get price data
            quotes = chart_data.get("indicators", {}).get("quote", [{}])[0]
            close_prices = quotes.get("close", [])

            # Filter out None values
            close_prices = [p for p in close_prices if p is not None]

            if len(close_prices) >= 2:
                start_price = close_prices[0]
                end_price = close_prices[-1]
                price_change = end_price - start_price
                percent_change = (price_change / start_price) * 100

                result = {
                    "ticker": ticker.upper(),
                    "period": period,
                    "start_price": round(start_price, 2),
                    "end_price": round(end_price, 2),
                    "price_change": round(price_change, 2),
                    "percent_change": round(percent_change, 2),
                    "trend": "up" if price_change > 0 else "down" if price_change < 0 else "flat"
                }

                return json.dumps(result, indent=2)
            else:
                return json.dumps({
                    "error": "Insufficient price data",
                    "ticker": ticker
                })
        else:
            return json.dumps({
                "error": f"Failed to fetch price data for {ticker}",
                "status_code": response.status_code
            })

    except Exception as e:
        return json.dumps({
            "error": f"Error calculating price change: {str(e)}",
            "ticker": ticker
        })


@tool
def compare_stocks(tickers: str) -> str:
    """
    Compare multiple stocks side by side.

    Args:
        tickers: Comma-separated list of ticker symbols (e.g., 'AAPL,GOOGL,MSFT')

    Returns:
        JSON string with comparative data for all provided stocks.

    Example:
        compare_stocks("AAPL,GOOGL,MSFT") -> Returns comparison of Apple, Google, and Microsoft
    """
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(",")]

        comparisons = []
        for ticker in ticker_list:
            # Fetch basic quote for each stock
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            params = {
                "interval": "1d",
                "range": "1d"
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                chart_data = data.get("chart", {}).get("result", [{}])[0]
                meta = chart_data.get("meta", {})

                comparisons.append({
                    "ticker": ticker,
                    "current_price": meta.get("regularMarketPrice"),
                    "previous_close": meta.get("previousClose"),
                    "day_change_percent": round(
                        ((meta.get("regularMarketPrice", 0) - meta.get("previousClose", 1)) /
                         meta.get("previousClose", 1)) * 100, 2
                    ) if meta.get("previousClose") else None,
                    "volume": meta.get("regularMarketVolume")
                })

        return json.dumps({
            "comparison": comparisons,
            "count": len(comparisons)
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "error": f"Error comparing stocks: {str(e)}",
            "tickers": tickers
        })


# Export all tools
STOCK_TOOLS = [
    get_stock_quote,
    search_stock_news,
    calculate_price_change,
    compare_stocks
]
