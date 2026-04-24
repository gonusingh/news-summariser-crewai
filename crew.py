 # ============================================================
# crew.py
# ------------------------------------------------------------
# Assembles agents and tasks into working crew
# NOTE: Fact Checker agent removed temporarily
# Reason: Groq free tier token limit (12k TPM)
# Add back when upgrading to paid tier!
# ============================================================

 # crew.py
# ============================================================
# Assembles agents and tasks into working Crew
# ------------------------------------------------------------
# CLEAN IMPORT: from agents import ...
# agents/ folder is now a proper Python package!
# Adding new agent = just add file + update __init__.py
# ============================================================

from crewai import Crew, Process

# Clean import from agents package!
from agents import (
    news_collector,
    news_filter,
    news_summariser
    # news_fact_checker  ← disabled: Groq token limit
)

from tasks import (
    collect_news_task,
    filter_news_task,
    summarise_news_task
)

news_crew = Crew(
    agents=[
        news_collector,
        news_filter,
        news_summariser
    ],
    tasks=[
        collect_news_task,
        filter_news_task,
        summarise_news_task
    ],
    process=Process.sequential,
    verbose=True
)