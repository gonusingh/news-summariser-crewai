# ============================================================
# main.py
# ------------------------------------------------------------
# This is the ENTRY POINT of our application
# Run this file every morning to get your news summary!
# Command: python main.py
# ============================================================


# ────────────────────────────────────────
# SECTION 1 — IMPORTS
# ────────────────────────────────────────

# Import our assembled crew from crew.py
from crew import news_crew

# datetime — to show today's date in output
from datetime import datetime


# ────────────────────────────────────────
# SECTION 2 — RUN THE CREW
# ────────────────────────────────────────

def run_news_summariser():
    """
    Main function that kicks off the entire crew.
    Call this every morning for your news briefing!
    """

    # Get today's date for display
    today = datetime.now().strftime("%A, %d %B %Y")

    # Print welcome header
    print("\n" + "=" * 50)
    print(f"   🗞️  MORNING NEWS SUMMARISER")
    print(f"   📅  {today}")
    print("=" * 50 + "\n")

    print("⏳ Starting your news crew...")
    print("   This may take 2-3 minutes")
    print("   Agents are working hard! 🤖\n")

    # kickoff() starts the entire crew!
    # This triggers all 4 agents and 4 tasks
    # in sequential order!
    result = news_crew.kickoff()

    # Print final output
    print("\n" + "=" * 50)
    print("   ✅  YOUR MORNING BRIEFING IS READY!")
    print("=" * 50 + "\n")

    # result.raw contains the final text output
    # from the last task (fact_check_task)
    print(result.raw)

    print("\n" + "=" * 50)
    print("   Have a productive day Vinit! 💪")
    print("=" * 50 + "\n")


# ────────────────────────────────────────
# SECTION 3 — ENTRY POINT
# ────────────────────────────────────────

# This checks if file is run directly
# vs imported by another file
#
# If run directly → run_news_summariser() runs
# If imported → nothing runs automatically
#
# This is Python best practice!
if __name__ == "__main__":
    run_news_summariser()