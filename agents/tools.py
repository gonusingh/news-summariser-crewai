# ============================================================
# agents/tools.py
# ------------------------------------------------------------
# PURPOSE: Shared tools that agents can use as superpowers
#
# WHAT IS A TOOL?
# LLMs cannot access the internet by themselves
# They only know what they were trained on (old data!)
# Tools give agents superpowers they don't naturally have:
# → search_news gives agents LIVE internet access!
#
# WHY SEPARATE FILE?
# Agent 1 (Collector) AND Agent 4 (Fact Checker)
# both need the search_news tool
# Define it ONCE here → import anywhere!
# Adding new tool tomorrow? Just add it here!
#
# HOW @tool DECORATOR WORKS:
# Step 1 → We write a normal Python function
# Step 2 → @tool wraps it and gives it an ID card
# Step 3 → Agents can now SEE and CALL this function
# Step 4 → Agent decides WHEN to call it (ReAct loop)
#
# ⚠️ CRITICAL RULE: Only ONE @tool decorator per function!
# Two decorators on same function = TypeError crash!
# ============================================================

# @tool decorator converts normal Python function
# into a CrewAI compatible tool agents can discover and call
from crewai.tools import tool

# DDGS = DuckDuckGo Search class
# New package name! Old name was duckduckgo_search
# Install: pip install ddgs
from ddgs import DDGS

# time module for adding delays between searches
# DuckDuckGo blocks too many fast requests (rate limiting)
# time.sleep(3) = pause 3 seconds between each search
import time


# ────────────────────────────────────────
# SEARCH NEWS TOOL
# ────────────────────────────────────────

# @tool decorator makes this function visible to agents
# "Search News Tool" = the name agents use to identify it
# The docstring below becomes the tool's description
# Agents read this description to decide when to use it!
@tool("Search News Tool")
def search_news(query: str) -> str:
    """
    Search for latest news using DuckDuckGo.
    Use this to find current news articles.
    Input should be a search query string.

    Args:
        query (str): what to search for
                     Example: "AI news today 2026"

    Returns:
        str: formatted news results with title, source,
             url and summary for each article found
             OR error message if search fails
    """

    try:
        # Create DuckDuckGo search instance
        # DDGS() = new class name (renamed from DDGS in old package)
        ddgs = DDGS()

        # WHY time.sleep(3)?
        # DuckDuckGo has a rate limit on free requests
        # If we search too many times too fast →
        # DuckDuckGo returns 403 Ratelimit error
        # 3 second pause between searches prevents this!
        # This was a real bug we fixed during development!
        time.sleep(3)

        # Search for news articles
        # query → what to search (passed by the agent)
        # max_results=3 → only fetch 3 results per search
        #
        # WHY 3 and not 5?
        # → Fewer results = fewer tokens used
        # → Groq free tier has 12,000 token/minute limit
        # → 3 good results beats 5 mediocre ones!
        results = ddgs.news(query, max_results=3)

        # Safety check: if search returns empty results
        # Return a helpful message instead of crashing
        # Agent reads this and tries a different search query!
        if not results:
            return f"No news found for: {query}"

        # Format each result into clean readable text
        # Agent reads this formatted text to extract info
        # Each result dictionary has: title, source, url, body
        formatted = ""
        for r in results:
            formatted += f"Title: {r['title']}\n"
            formatted += f"Source: {r['source']}\n"
            formatted += f"URL: {r['url']}\n"
            formatted += f"Summary: {r['body']}\n"

            # Visual divider between results
            # Makes it easier for agent to parse each story
            formatted += "-" * 40 + "\n"

        return formatted

    except Exception as e:
        # WHY try/except?
        # If DuckDuckGo is down OR rate limits us →
        # we don't want the ENTIRE crew to crash!
        #
        # Instead → return friendly error message
        # Agent reads this, notes the failure, and
        # continues with whatever news it already has!
        # One failed search ≠ entire project failure!
        return f"Search temporarily unavailable: {str(e)}"