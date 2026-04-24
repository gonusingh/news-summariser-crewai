# ============================================================
# agents/__init__.py
# ------------------------------------------------------------
# PURPOSE: Makes agents/ folder a proper Python package
#
# WHY IS __init__.py NEEDED?
# Without __init__.py → Python doesn't recognise
#                       agents/ as a package at all
#                       → all imports will FAIL!
#
# With __init__.py    → Python treats agents/ as a package
#                       → clean imports work everywhere!
#
# WHAT DOES IT DO?
# Imports all agents from their individual files
# and makes them available at the package level
#
# This means in crew.py you can write:
# from agents import news_collector, news_filter, ...
# Instead of the messier:
# from agents.collector import news_collector
# from agents.filter import news_filter
# etc.
#
# HOW TO ADD A NEW AGENT:
# Step 1: Create agents/new_agent.py
# Step 2: Define the agent inside it
# Step 3: Add import here → from agents.new_agent import ...
# Step 4: Add to __all__ list below
# Step 5: Import in crew.py → DONE! Clean and scalable!
#
# This is the SCALABLE ARCHITECTURE your mentor requested!
# ============================================================

# Import each agent from its own dedicated file
# Each file has ONE agent = clean separation of concerns!
from agents.collector import news_collector
from agents.filter import news_filter
from agents.summariser import news_summariser
from agents.fact_checker import news_fact_checker

# __all__ explicitly declares what this package exports
# When someone writes "from agents import *"
# only these names will be imported
# Good practice for clean, explicit public APIs!
__all__ = [
    "news_collector",    # Agent 1 — searches internet for news
    "news_filter",       # Agent 2 — filters relevant stories
    "news_summariser",   # Agent 3 — writes morning briefing
    "news_fact_checker"  # Agent 4 — verifies URLs (disabled)
]