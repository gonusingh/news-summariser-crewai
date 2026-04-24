# ============================================================
# agents/summariser.py
# ------------------------------------------------------------
# PURPOSE: Define Agent 3 — the News Summariser
#
# AGENT 3 DETAILS:
# Job:    Write clean, friendly morning news briefing
# Tools:  NONE — pure writing task, no internet needed
# Input:  Filtered news from Agent 2 (passed via context)
# Output: Beautiful formatted morning summary with emojis
#
# FLOW POSITION:
# Agent 1 → Agent 2 → [Agent 3 Summariser]
#
# WHY NO TOOL?
# Agent 3 is a WRITER not a researcher!
# It receives already-filtered stories and rewrites them
# in simple, friendly, easy-to-read language
# No internet access needed — just excellent writing!
#
# WRITING STYLE:
# The backstory carefully shapes the writing style:
# → "10,000 subscribers" → writes for scale and clarity
# → "5 minutes" → keeps it short and scannable
# → "smart friend" → casual, not formal or corporate
# → "no jargon" → simple English for everyone
# → "emojis" → friendly and visually scannable
# ============================================================

from crewai import Agent
from .llm import llm


# ────────────────────────────────────────
# AGENT 3 — NEWS SUMMARISER
# ────────────────────────────────────────

news_summariser = Agent(

    role="Morning Newsletter Writer",

    # Goal defines the FORMAT and RULES of the output
    # Very specific expected output = very consistent results!
    # Notice:
    # → "2-3 lines maximum" = hard length limit per story
    # → "source URL" = must include for credibility
    # → "BREAKING NEWS at top" = crisis priority rule
    goal=(
        "Write a clean, friendly and easy to understand "
        "morning news briefing from the filtered stories. "
        "Keep each story summary to 2-3 lines maximum. "
        "Always include source URL so readers can read more. "
        "Put BREAKING NEWS at top with 🚨 emoji if it exists."
    ),

    # Backstory shapes the WRITING STYLE and TONE
    # Every detail here influences how the LLM writes:
    #
    # "10,000 subscribers" → writes with responsibility and clarity
    # "5 minutes" → reader is time-poor, every word counts!
    # "smart friend" → conversational, not stiff or corporate
    # "no jargon" → accessible to everyone, not just experts
    # "emojis" → visual cues help readers scan quickly
    #
    # This is Prompt Engineering at work!
    # The backstory IS the writing style guide for the LLM
    backstory=(
        "You write the morning briefing for 10,000 busy "
        "subscribers every single day. "
        "You are famous for making complex news simple, "
        "short and genuinely interesting to read. "
        "You write like you are talking to a smart friend "
        "— no jargon, no corporate fluff, no unnecessary words. "
        "Your readers have only 5 minutes every morning "
        "so every single word in your briefing must count. "
        "You use emojis naturally to make it friendly "
        "and easy to scan quickly."
    ),

    # No tools needed — Agent 3 is purely a writing agent
    # It transforms filtered text into beautiful summaries
    # All data comes from Agent 2 via context passing
    tools=[],

    llm=llm,
    verbose=True,
    use_system_prompt=False
)