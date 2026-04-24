# ============================================================
# agents/collector.py
# ------------------------------------------------------------
# PURPOSE: Define Agent 1 — the News Collector
#
# WHAT IS AN AGENT?
# An agent is an AI employee with:
# → role      = job title (who they are)
# → goal      = what they want to achieve
# → backstory = their experience (shapes LLM behaviour!)
# → tools     = superpowers they can use
# → llm       = the brain they think with
#
# AGENT 1 DETAILS:
# Job:    Search internet for today's top 5 news stories
# Tools:  search_news (needs internet access)
# Input:  Nothing — first agent, starts completely fresh
# Output: Raw headlines + source names + URLs + summaries
#
# FLOW POSITION:
# [Agent 1 Collector] → Agent 2 Filter → Agent 3 Summariser
#
# WHY NEEDS TOOL?
# Agent 1 must fetch LIVE news — LLM alone only knows
# old training data. search_news gives real-time access!
#
# HOW BACKSTORY WORKS:
# The backstory is a PROMPT that shapes LLM behaviour
# LLM literally roleplays as that character!
# More detailed backstory = more focused, reliable output
# "15 years at Reuters" → LLM acts like a real journalist!
# ============================================================

# Agent class — the base class to create any AI agent
from crewai import Agent

# Relative imports from same agents/ folder
# The dot (.) means "from current package folder"
# agents/tools.py → provides search_news tool
# agents/llm.py   → provides shared LLM brain
from .tools import search_news
from .llm import llm


# ────────────────────────────────────────
# AGENT 1 — NEWS COLLECTOR
# ────────────────────────────────────────

news_collector = Agent(

    # role = job title shown in terminal logs during execution
    # Also helps LLM understand its professional identity!
    # Be specific — "Senior News Research Journalist" is better
    # than just "Journalist" because it implies expertise level
    role="Senior News Research Journalist",

    # goal = what this agent is trying to achieve
    # This guides the LLM's decision-making throughout the task
    # Be SPECIFIC — vague goals = vague, unreliable results!
    #
    # BAD:  "find news"
    # GOOD: "find top 5 AI and tech news with source URLs"
    goal=(
        "Find today's top 5 most important news stories "
        "covering AI, technology, global affairs and science. "
        "Always include the source URL for every story found."
    ),

    # backstory = the PROMPT that shapes how LLM behaves
    # LLM literally ROLEPLAYS as this character!
    # Think of it as intensive job training for the LLM
    #
    # Notice we mention:
    # → Years of experience (builds credibility and authority)
    # → Specific employers (Reuters, BBC = trusted sources)
    # → Key rules (NEVER make up news = anti-hallucination!)
    # → URL requirement (grounding = prevents fake stories)
    #
    # The more detailed and specific the backstory →
    # the more focused and professional the agent's output!
    backstory=(
        "You are a senior journalist with 15 years of "
        "experience at Reuters and BBC News. "
        "You have a sharp eye for identifying important stories "
        "and always find news from credible, trusted sources. "
        "You NEVER make up or fabricate news — you only report "
        "what you actually find from real online sources. "
        "You always include the source URL with every story "
        "because your readers need to verify information themselves."
    ),

    # tools = list of superpowers this agent can use
    # Agent 1 NEEDS search_news to access live internet
    # The agent DECIDES when and how to use this tool!
    # We don't tell it HOW — it figures out itself (ReAct!)
    # This is what makes it an AGENT not just a script!
    tools=[search_news],

    # llm = the brain this agent thinks with
    # Imported from agents/llm.py — shared across all agents
    # All agents share same LLM but behave differently because
    # of their unique role + goal + backstory (job training!)
    llm=llm,

    # verbose=True → prints agent's thinking to terminal
    # Shows: what tool it called, what it searched for,
    #        what decision it made, what it produced
    #
    # Keep True during DEVELOPMENT for debugging and learning
    # Set False in PRODUCTION for cleaner user experience
    verbose=True,

    # use_system_prompt=False → fixes Groq tool calling issue
    # Groq's Llama model had compatibility issues with CrewAI's
    # native tool calling format → this forces ReAct style
    # which works reliably with Groq's free tier models
    # This was a real bug we discovered and fixed!
    use_system_prompt=False
)