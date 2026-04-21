# ============================================================
# agents.py
# ------------------------------------------------------------
# PURPOSE: Define all 4 AI agents for Morning News Summariser
#
# WHAT IS AN AGENT?
# An agent is like a smart employee with:
#   - role      → job title (who they are)
#   - goal      → what they want to achieve
#   - backstory → their experience (shapes behaviour)
#   - tools     → superpowers they can use
#   - llm       → the brain they think with
#
# OUR 4 AGENTS:
#   1. News Collector   → searches internet for news
#   2. News Filter      → picks most relevant stories
#   3. News Summariser  → writes clean morning briefing
#   4. Fact Checker     → verifies every story is real
# ============================================================


# ────────────────────────────────────────
# SECTION 1 — IMPORTS
# ────────────────────────────────────────

# Agent  → base class to create any AI agent
# LLM    → connects CrewAI to external LLM provider
#          (in our case — Groq)
from crewai import Agent, LLM

# @tool decorator → converts a normal Python function
# into a CrewAI compatible tool that agents can call
# Without @tool → agents cannot discover or use
# the function at all!
from crewai.tools import tool

# DDGS → DuckDuckGo Search class
# This is the actual library that hits
# DuckDuckGo and returns news results
# Completely FREE — no API key needed!
from ddgs import DDGS

# load_dotenv → reads our .env file and loads
# all key=value pairs into environment memory
# Must be called BEFORE os.getenv()!
from dotenv import load_dotenv

# os → used to read environment variables
# os.getenv("KEY") reads from loaded .env memory
import os

# time → used to add delays between searches
# DuckDuckGo blocks too many fast requests
# time.sleep(3) pauses 3 seconds between searches
import time

# ────────────────────────────────────────
# LOAD ENVIRONMENT VARIABLES
# ────────────────────────────────────────

# This reads .env file and loads GROQ_API_KEY
# into memory so os.getenv() can access it
#
# ORDER MATTERS:
# load_dotenv() FIRST → then os.getenv()
# If reversed → os.getenv returns None
# because .env hasn't been loaded yet!
load_dotenv()


# ────────────────────────────────────────
# SECTION 2 — CUSTOM SEARCH TOOL
# ────────────────────────────────────────

# WHY DO WE NEED A CUSTOM TOOL?
# LLMs cannot access internet by themselves
# They only know what they were trained on
# To get LIVE news → we give them a search tool
#
# HOW @tool WORKS:
# Step 1 → We write a normal Python function
# Step 2 → @tool wraps it and gives it an ID card
# Step 3 → Agents can now SEE and CALL this function
# Step 4 → Agent decides WHEN to call it (ReAct loop)
#
# IMPORTANT: Only ONE @tool decorator per function!
# Two decorators on same function = TypeError crash!

@tool("Search News Tool")
def search_news(query: str) -> str:
    """
    Search for latest news using DuckDuckGo.
    Use this to find current news articles.
    Input should be a search query string.

    Args:
        query (str): what to search for
                     example: "AI news today"

    Returns:
        str: formatted news results with
             title, source, url and summary
             OR error message if search fails
    """

    try:
        # Create DuckDuckGo search instance
        # DDGS = DuckDuckGo Search (new package name)
        # Old name was duckduckgo_search — now renamed!
        ddgs = DDGS()

        # WHY time.sleep(3)?
        # DuckDuckGo has a rate limit — if we search
        # too many times too fast it returns 403 error
        # 3 second pause between searches prevents this!
        time.sleep(3)

        # Search for news articles
        # max_results=3 → only 3 results per search
        # Why 3 and not 5?
        # → Fewer requests = less rate limit risk
        # → 3 good results beats 5 mediocre ones
        results = ddgs.news(query, max_results=3)

        # Safety check — if search returns nothing
        # return helpful message instead of crashing
        # Agent reads this and tries a different query!
        if not results:
            return f"No news found for: {query}"

        # Format each result into clean readable text
        # Agent reads this formatted text to extract info
        # Each result has: title, source, url, body
        formatted = ""
        for r in results:
            formatted += f"Title: {r['title']}\n"
            formatted += f"Source: {r['source']}\n"
            formatted += f"URL: {r['url']}\n"
            formatted += f"Summary: {r['body']}\n"

            # Divider between results for readability
            formatted += "-" * 40 + "\n"

        return formatted

    except Exception as e:
        # WHY try/except?
        # If DuckDuckGo is down or rate limits us
        # we don't want the ENTIRE crew to crash!
        # Instead → return friendly error message
        # Agent reads this and continues with
        # whatever news it already has collected!
        return f"Search temporarily unavailable: {str(e)}"


# ────────────────────────────────────────
# SECTION 3 — LLM SETUP
# ────────────────────────────────────────

# WHY DO WE NEED AN LLM?
# LLM = the BRAIN of every agent
# Without LLM → agent cannot think, reason or decide
# All 4 agents SHARE this same LLM instance
# But behave DIFFERENTLY because of their unique
# role + goal + backstory (their job training!)
#
# ANALOGY:
# Same human brain → different jobs
# Doctor vs Lawyer → both use same brain type
# but trained completely differently!
#
# WHY GROQ?
# → Free tier available (perfect for learning!)
# → Very fast response times
# → Supports Llama models (open source + powerful)
# → Easy to set up with CrewAI

 # ────────────────────────────────────────
# LLM SETUP
# ────────────────────────────────────────

# WHY these extra settings?
# Groq + Llama has a known issue with
# CrewAI's native tool calling format
# Setting these fixes the compatibility!

llm = LLM(
    # Current active Groq model
    model="groq/llama-3.3-70b-versatile",

    # API key from .env file
    api_key=os.getenv("GROQ_API_KEY"),

    # Temperature controls creativity
    # 0.1 = focused and factual (good for news!)
    # 1.0 = very creative and random
    temperature=0.1
)


# ────────────────────────────────────────
# SECTION 4 — AGENT 1: NEWS COLLECTOR
# ────────────────────────────────────────
#
# JOB:    Search internet for today's top news
# TOOLS:  search_news (needs internet access)
# INPUT:  nothing — this is the FIRST agent
# OUTPUT: raw news headlines + URLs + summaries
#
# FLOW POSITION:
# [Agent 1] → Agent 2 → Agent 3 → Agent 4
#
# WHY NEEDS TOOL?
# Agent 1 must fetch LIVE news from internet
# LLM alone only knows old training data
# search_news tool gives it real-time access!

news_collector = Agent(
    # role = job title shown in terminal logs
    # Also helps LLM understand its identity!
    role="Senior News Research Journalist",

    # goal = what this agent is trying to achieve
    # Be SPECIFIC — vague goals = vague results!
    # Bad:  "find news"
    # Good: "find top 5 AI and tech news with URLs"
    goal=(
        "Find today's top 5 most important news stories "
        "covering AI, technology, global affairs and science. "
        "Always include the source URL for every story."
    ),

    # backstory = the PROMPT that shapes agent behaviour
    # LLM literally ROLEPLAYS as this character!
    # More detailed backstory = more focused behaviour
    #
    # Notice we mention:
    # → Years of experience (builds authority)
    # → Where they worked (BBC, Reuters = credible)
    # → Key rule (NEVER make up news = anti-hallucination)
    backstory=(
        "You are a senior journalist with 15 years of "
        "experience at Reuters and BBC News. "
        "You have a sharp eye for important stories and "
        "always find news from credible sources. "
        "You NEVER make up news — you only report what "
        "you actually find from real online sources. "
        "You always include the source URL with every story "
        "because your readers need to verify information."
    ),

    # tools = list of superpowers agent can use
    # Agent 1 needs search_news to access internet
    # Agent DECIDES when and how to use this tool!
    # We don't tell it — it figures out itself (ReAct!)
    tools=[search_news],

    # llm = the brain this agent thinks with
    # All agents share same LLM but behave differently
    # because of their unique role+goal+backstory!
    llm=llm,

    # verbose=True → prints agent's thinking to terminal
    # Shows: what tool it called, what it searched,
    #        what decision it made, what it produced
    # Keep True during DEVELOPMENT for debugging
    # Set False in PRODUCTION for cleaner output
    verbose=True,
    use_system_prompt=False

)


# ────────────────────────────────────────
# SECTION 5 — AGENT 2: NEWS FILTER
# ────────────────────────────────────────
#
# JOB:    Read Agent 1 output, keep only best news
# TOOLS:  NONE — works on text, no internet needed
# INPUT:  raw news from Agent 1 (via context)
# OUTPUT: top 3-5 most relevant filtered stories
#
# FLOW POSITION:
# Agent 1 → [Agent 2] → Agent 3 → Agent 4
#
# WHY NO TOOL?
# Agent 2 doesn't need internet!
# It only reads what Agent 1 already collected
# and uses LLM brain to decide what's relevant
# Pure reasoning task — no external data needed!

news_filter = Agent(
    role="Senior News Editor",

    goal=(
        "Filter and select only the most relevant and "
        "important news stories from what was collected. "
        "Focus on AI, technology, global affairs and science. "
        "Remove irrelevant, duplicate or low quality news. "
        "If any crisis or disaster story exists — "
        "mark it as BREAKING NEWS and put it FIRST!"
    ),

    # Backstory defines WHO filters and WHY
    # Notice: we mention the TARGET READER
    # "young tech professionals in India"
    # This makes agent filter for THAT specific audience!
    backstory=(
        "You are a senior editor at a top technology "
        "magazine with 10 years of experience. "
        "Your readers are busy young tech professionals "
        "in India who want to stay updated on what truly "
        "matters in AI, technology and global affairs. "
        "You ruthlessly cut irrelevant stories and keep "
        "only news that has real impact on their lives. "
        "You never add news that wasn't in original list — "
        "you only filter, never fabricate!"
    ),

    # Empty list = no tools needed
    # Agent 2 uses only its LLM brain to reason
    tools=[],
    llm=llm,
    verbose=True,
    use_system_prompt=False

)


# ────────────────────────────────────────
# SECTION 6 — AGENT 3: NEWS SUMMARISER
# ────────────────────────────────────────
#
# JOB:    Write clean friendly morning briefing
# TOOLS:  NONE — pure writing task
# INPUT:  filtered news from Agent 2 (via context)
# OUTPUT: beautiful formatted morning summary
#
# FLOW POSITION:
# Agent 1 → Agent 2 → [Agent 3] → Agent 4
#
# WHY NO TOOL?
# Agent 3 is a WRITER not a researcher
# It takes filtered stories and rewrites them
# in simple friendly language
# No internet access needed — just good writing!

news_summariser = Agent(
    role="Morning Newsletter Writer",

    goal=(
        "Write a clean, friendly and easy to understand "
        "morning news briefing from the filtered stories. "
        "Keep each story summary to 2-3 lines maximum. "
        "Always include source URL so readers can read more. "
        "Put BREAKING NEWS at top with 🚨 emoji if exists."
    ),

    # Backstory shapes WRITING STYLE of agent!
    # Notice key details:
    # → "10,000 subscribers" → writes for scale
    # → "5 minutes" → knows readers are busy
    # → "smart friend" → casual not formal tone
    # → "no jargon" → simple language rule
    backstory=(
        "You write the morning briefing for 10,000 busy "
        "subscribers every single day. "
        "You are famous for making complex news simple, "
        "short and interesting to read. "
        "You write like you are talking to a smart friend "
        "— no jargon, no fluff, no unnecessary words. "
        "Your readers have only 5 minutes every morning "
        "so every single word in your briefing must count. "
        "You use emojis to make it friendly and scannable."
    ),

    tools=[],
    llm=llm,
    verbose=True,
    use_system_prompt=False

)


# ────────────────────────────────────────
# SECTION 7 — AGENT 4: FACT CHECKER
# ────────────────────────────────────────
#
# JOB:    Verify every story has a real source URL
# TOOLS:  search_news (needs to verify online)
# INPUT:  summarised briefing from Agent 3 (via context)
# OUTPUT: final verified news briefing
#
# FLOW POSITION:
# Agent 1 → Agent 2 → Agent 3 → [Agent 4]
#
# WHY THIS AGENT EXISTS — THE HALLUCINATION PROBLEM:
# LLMs can sometimes MAKE UP news that doesn't exist
# This is called hallucination!
# Agent 4 is our last line of defence —
# it searches every story online to verify it's real
# No URL found = story gets REMOVED from final output
#
# WHY NEEDS TOOL?
# Must go online to verify URLs actually exist
# Cannot verify internet sources without internet!
# Same tool as Agent 1 but used for VERIFICATION
# not collection — same tool, different purpose!
#
# THIS WAS VINIT'S IDEA! 🎯
# Great engineering instinct to add this layer!

news_fact_checker = Agent(
    role="News Fact Verification Journalist",

    goal=(
        "Verify that every news story in the summary "
        "has a real and working source URL. "
        "Search online to confirm each story exists. "
        "Remove any story that cannot be verified. "
        "Return only verified trustworthy news stories."
    ),

    # Backstory makes agent OBSESSIVE about facts
    # Notice: "zero tolerance" and "No URL = No story"
    # These strong phrases make LLM strict and thorough!
    backstory=(
        "You are an obsessive fact checker with zero "
        "tolerance for fake or unverified news. "
        "You have worked at FactCheck.org for 8 years "
        "and have caught hundreds of fake stories. "
        "Your golden rule that you never break: "
        "No URL = No story. Period. "
        "Every claim must trace back to a real source. "
        "You protect thousands of readers from "
        "misinformation every single day."
    ),

    # Fact checker needs search tool to verify URLs!
    # Same tool as Agent 1 but used differently —
    # Agent 1 uses it to FIND news
    # Agent 4 uses it to VERIFY news exists
    tools=[search_news],
    llm=llm,
    verbose=True,
    use_system_prompt=False

)