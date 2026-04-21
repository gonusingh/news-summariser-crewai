# ============================================================
# tasks.py
# ------------------------------------------------------------
# This file defines ALL 4 tasks for our News Summariser
# Think of this as "Work Orders" given to each agent
# Each task has a description, expected output and agent
# ============================================================


# ────────────────────────────────────────
# SECTION 1 — IMPORTS
# ────────────────────────────────────────

# Task class — used to create each task
from crewai import Task

# Import all 4 agents we created in agents.py
# Tasks need to know WHICH agent does WHAT!
from agents import (
    news_collector,
    news_filter,
    news_summariser,
    news_fact_checker
)


# ────────────────────────────────────────
# SECTION 2 — TASK 1: COLLECT NEWS
# ────────────────────────────────────────

# This task is assigned to news_collector agent
# It is the FIRST task — no context needed
# Output of this task → becomes input of Task 2

collect_news_task = Task(
    # Description = exact instructions for the agent
    # More specific = better quality output!
    description=(
        "Search the internet and find today's top 5 "
        "most important news stories. "
        "Focus ONLY on these topics: "
        "1. Artificial Intelligence and Technology "
        "2. Global Affairs and World Events "
        "3. Science and Innovation "
        "4. Any major crisis or breaking news "
        "\n\n"
        "For EACH news story you must find: "
        "- Full headline "
        "- Brief description of what happened "
        "- Source name (Times of India, BBC, TechCrunch etc) "
        "- Source URL (this is mandatory!) "
        "\n\n"
        "IMPORTANT: Do NOT make up any news. "
        "Only report what you actually find online."
    ),

    # Expected output = what the result should look like
    # This guides the LLM on HOW to format its answer
    expected_output=(
        "A list of exactly 5 news stories with: "
        "- Headline "
        "- 2-3 line description "
        "- Source name "
        "- Source URL "
        "Formatted clearly and separated by dividers."
    ),

    # Which agent does this task
    agent=news_collector,

    # context = None because this is first task
    # No previous task output to read from!
)


# ────────────────────────────────────────
# SECTION 3 — TASK 2: FILTER NEWS
# ────────────────────────────────────────

# This task is assigned to news_filter agent
# It READS output from Task 1 via context!
# Context = how tasks pass information to each other

filter_news_task = Task(
    description=(
        "Read the news stories collected by the journalist. "
        "Your job is to filter and keep only the most "
        "relevant and important stories. "
        "\n\n"
        "KEEP stories about: "
        "- Artificial Intelligence breakthroughs "
        "- Major global events or crises "
        "- Important science discoveries "
        "- Technology that impacts society "
        "\n\n"
        "REMOVE stories about: "
        "- Celebrity gossip or entertainment "
        "- Sports (unless major world event) "
        "- Local news with no global impact "
        "- Duplicate or very similar stories "
        "\n\n"
        "IMPORTANT RULE: "
        "If a major national or global CRISIS exists "
        "in the collected news — mark it clearly as "
        "BREAKING NEWS and put it FIRST in your list! "
        "This was your idea Vinit — great thinking! 🎯"
    ),

    expected_output=(
        "A filtered list of top 3 to 5 news stories. "
        "Each story must have: "
        "- Headline "
        "- 2-3 line description "
        "- Source name and URL "
        "- BREAKING tag if it is a crisis story "
        "Stories ordered by importance — "
        "most important first!"
    ),

    agent=news_filter,

    # context tells CrewAI —
    # "before running this task, give the agent
    #  the output from collect_news_task"
    # This is how agents talk to each other!
    context=[collect_news_task]
)


# ────────────────────────────────────────
# SECTION 4 — TASK 3: SUMMARISE NEWS
# ────────────────────────────────────────

# This task is assigned to news_summariser agent
# It reads filtered news from Task 2
# and writes a clean morning briefing!

summarise_news_task = Task(
    description=(
        "Read the filtered news stories from the editor. "
        "Write a clean, friendly morning news briefing "
        "that busy people can read in under 5 minutes. "
        "\n\n"
        "Format your briefing like this: "
        "- Start with a friendly good morning greeting "
        "- If any BREAKING NEWS exists — show it FIRST "
        "  with a 🚨 emoji "
        "- Then show remaining news stories "
        "- End with a motivating one liner "
        "\n\n"
        "Writing rules: "
        "- Use simple English — no jargon "
        "- Maximum 3 lines per story "
        "- Always include source URL "
        "- Use emojis to make it friendly "
        "- Write like talking to a smart friend"
    ),

    expected_output=(
        "A beautiful morning news briefing with: "
        "- Good morning greeting "
        "- 3 to 5 news stories with emojis "
        "- Each story: headline + 2-3 lines + URL "
        "- BREAKING NEWS at top if crisis exists "
        "- Motivating closing line "
        "Easy to read, friendly and informative!"
    ),

    agent=news_summariser,

    # Reads filtered output from Task 2
    context=[filter_news_task]
)


# ────────────────────────────────────────
# SECTION 5 — TASK 4: FACT CHECK
# ────────────────────────────────────────

# This task is assigned to news_fact_checker agent
# It verifies every story has a real URL
# Last line of defence against hallucination!
# YOUR idea Vinit! 🎯

fact_check_task = Task(
    description=(
        "Read the morning news briefing carefully. "
        "Your job is to verify every single news story "
        "has a real and working source URL. "
        "\n\n"
        "For each story: "
        "- Search the headline online "
        "- Check if the story actually exists "
        "- Verify the source URL is real "
        "\n\n"
        "If story is VERIFIED → keep it in final output "
        "If story CANNOT be verified → remove it completely "
        "\n\n"
        "GOLDEN RULE: No URL = No story! "
        "Protect readers from fake news at all costs."
    ),

    expected_output=(
        "The final verified morning news briefing. "
        "Same format as input but: "
        "- Only verified stories remain "
        "- Each story has a confirmed working URL "
        "- Any fake or unverifiable story is removed "
        "- Add VERIFIED tag next to each story "
        "This is the final output shown to the user!"
    ),

    agent=news_fact_checker,

    # Reads summarised briefing from Task 3
    context=[summarise_news_task]
)