# ============================================================
# agents/fact_checker.py
# ------------------------------------------------------------
# PURPOSE: Define Agent 4 — the Fact Checker
#
# AGENT 4 DETAILS:
# Job:    Verify every story has a real working source URL
# Tools:  search_news (needs internet to verify URLs)
# Input:  Summary from Agent 3 (passed via context)
# Output: Final verified morning briefing
#
# FLOW POSITION:
# Agent 1 → Agent 2 → Agent 3 → [Agent 4 Fact Checker]
#
# ⚠️ CURRENT STATUS: Built and ready but DISABLED in crew.py
# REASON: Groq free tier = 12,000 tokens per minute limit
#         Running 4 agents exceeds this limit consistently
#         Agent 4 uses many tokens verifying each URL
# PLAN:   Re-enable when upgrading to Groq paid tier
#         OR switch to Gemini API (higher free tier limits)
#
# WHY THIS AGENT EXISTS — THE HALLUCINATION PROBLEM:
# LLMs sometimes MAKE UP news stories that don't exist
# This is called hallucination — very dangerous for news!
# Agent 4 is our last line of defence against fake news
# It searches every story headline online to verify it exists
# If no real URL found → story is REMOVED from final output
# No URL = No story. Always.
#
# THIS WAS VINIT'S ORIGINAL IDEA! 🎯
# Added during architecture design before any code was written
# Great engineering instinct — shows depth of thinking!
#
# WHY NEEDS TOOL?
# Must go online to verify URLs actually exist on the internet
# Cannot verify internet sources without internet access!
# Same search_news tool as Agent 1 but used differently:
# Agent 1 uses it to FIND news stories
# Agent 4 uses it to VERIFY stories actually exist
# Same tool, completely different purpose!
# ============================================================

from crewai import Agent

# Import search tool — needed to verify URLs online
from .tools import search_news
from .llm import llm


# ────────────────────────────────────────
# AGENT 4 — FACT CHECKER
# ────────────────────────────────────────

news_fact_checker = Agent(

    role="News Fact Verification Journalist",

    # Goal is very strict and uncompromising
    # "remove any story that cannot be verified" = zero tolerance
    # This strictness is intentional and necessary!
    goal=(
        "Verify that every news story in the summary "
        "has a real and working source URL. "
        "Search online to confirm each story actually exists. "
        "Remove any story that cannot be verified online. "
        "Return only verified, trustworthy news stories."
    ),

    # Backstory makes agent OBSESSIVE about verification
    # Notice the strong, uncompromising language:
    # "zero tolerance" → no exceptions allowed
    # "No URL = No story. Period." → absolute rule
    # "8 years at FactCheck.org" → deep expertise
    #
    # Strong language in backstory = strict agent behaviour!
    # This intentional strictness protects readers from
    # misinformation and hallucinated fake news stories
    backstory=(
        "You are an obsessive fact checker with zero "
        "tolerance for fake, unverified or hallucinated news. "
        "You have worked at FactCheck.org for 8 years and "
        "have personally caught hundreds of fabricated stories. "
        "Your absolute golden rule that you NEVER break: "
        "No URL = No story. Period. No exceptions. Ever. "
        "Every single claim must trace back to a real, "
        "verifiable source on the internet. "
        "You protect thousands of readers from misinformation "
        "every single day and take this responsibility seriously."
    ),

    # search_news tool needed to verify each URL exists!
    # Agent 4 searches each story headline to confirm
    # the story can be found on real news websites
    # If search returns nothing → story gets removed!
    tools=[search_news],

    llm=llm,
    verbose=True,
    use_system_prompt=False
)