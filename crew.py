 # ============================================================
# crew.py
# ------------------------------------------------------------
# Assembles agents and tasks into working crew
# NOTE: Fact Checker agent removed temporarily
# Reason: Groq free tier token limit (12k TPM)
# Add back when upgrading to paid tier!
# ============================================================

from crewai import Crew, Process

# Import only 3 agents (fact checker removed)
from agents import (
    news_collector,
    news_filter,
    news_summariser
)

# Import only 3 tasks (fact check task removed)
from tasks import (
    collect_news_task,
    filter_news_task,
    summarise_news_task
)

# Assemble the crew with 3 agents
news_crew = Crew(
    agents=[
        news_collector,   # searches news
        news_filter,      # filters news
        news_summariser   # writes briefing
    ],

    tasks=[
        collect_news_task,    # Task 1
        filter_news_task,     # Task 2
        summarise_news_task   # Task 3
    ],

    # Sequential = one after another
    process=Process.sequential,
    verbose=True
)