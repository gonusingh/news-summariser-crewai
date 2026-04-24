# ============================================================
# agents/filter.py
# ------------------------------------------------------------
# PURPOSE: Define Agent 2 — the News Filter
#
# AGENT 2 DETAILS:
# Job:    Read Agent 1 output, keep only best stories
# Tools:  NONE — works purely on text, no internet needed
# Input:  Raw news from Agent 1 (passed via context)
# Output: Top 3-5 most relevant filtered stories
#
# FLOW POSITION:
# Agent 1 Collector → [Agent 2 Filter] → Agent 3 Summariser
#
# WHY NO TOOL?
# Agent 2 doesn't need internet at all!
# It only reads what Agent 1 already collected
# and uses LLM brain to judge what's relevant
# Pure reasoning task — no external data needed!
#
# HOW CONTEXT WORKS:
# tasks.py passes collect_news_task output as context
# Agent 2 automatically receives Agent 1's findings
# This is how agents "talk" to each other in CrewAI!
#
# CRISIS DETECTION:
# Agent 2 is responsible for identifying breaking news
# If any crisis/disaster story exists in collected news →
# it gets tagged as BREAKING NEWS and placed FIRST!
# This was Vinit's idea — great engineering instinct! 🎯
# ============================================================

from crewai import Agent
from .llm import llm


# ────────────────────────────────────────
# AGENT 2 — NEWS FILTER
# ────────────────────────────────────────

news_filter = Agent(

    role="Senior News Editor",

    # Goal defines what GOOD filtering means
    # Notice we specify:
    # → WHAT to keep (AI, tech, global affairs, science)
    # → BREAKING NEWS rule (crisis = goes FIRST!)
    # Being specific here prevents random filtering!
    goal=(
        "Filter and select only the most relevant and "
        "important news stories from what was collected. "
        "Focus on AI, technology, global affairs and science. "
        "Remove irrelevant, duplicate or low quality news. "
        "If any crisis or disaster story exists — "
        "mark it as BREAKING NEWS and put it FIRST!"
    ),

    # Backstory defines WHO is doing the filtering
    # and most importantly WHO they are filtering FOR!
    #
    # Notice the TARGET READER is defined:
    # "busy young tech professionals in India"
    # This makes the LLM filter for THAT specific audience!
    # Different audience = completely different filter criteria!
    #
    # Also notice: "never add news that wasn't in original list"
    # This prevents Agent 2 from hallucinating new stories!
    backstory=(
        "You are a senior editor at a top technology "
        "magazine with 10 years of experience. "
        "Your readers are busy young tech professionals "
        "in India who want to stay updated on what truly "
        "matters in AI, technology and global affairs. "
        "You ruthlessly cut irrelevant stories and keep "
        "only news that has real impact on their lives. "
        "You never add news that wasn't in the original list "
        "— you only filter, you never fabricate!"
    ),

    # Empty list = no tools needed!
    # Agent 2 is a pure reasoning/judgment agent
    # It works ONLY on text received from Agent 1
    # No internet access required for this job!
    tools=[],

    llm=llm,
    verbose=True,
    use_system_prompt=False
)