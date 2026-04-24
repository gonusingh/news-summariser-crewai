# ============================================================
# agents/llm.py
# ------------------------------------------------------------
# PURPOSE: Centralised LLM configuration for all agents
#
# WHY A SEPARATE FILE?
# All 4 agents share the same LLM brain
# If we need to change the model tomorrow →
# change here ONCE instead of in every agent file!
# This follows DRY principle = Don't Repeat Yourself
#
# HOW TO USE:
# from agents.llm import llm
# Then pass llm=llm in any Agent definition
# ============================================================

# LLM class connects CrewAI to external LLM providers
# Without this → agents have no brain to think with!
from crewai import LLM

# load_dotenv reads our .env file and loads all
# key=value pairs into environment memory
# MUST be called before os.getenv() !
from dotenv import load_dotenv

# os module lets us read environment variables
# os.getenv("KEY") reads from loaded .env memory
import os

# ────────────────────────────────────────
# LOAD ENVIRONMENT VARIABLES
# ────────────────────────────────────────

# This reads .env file and loads GROQ_API_KEY into memory
# ORDER MATTERS:
# Step 1: load_dotenv() → reads .env file into memory
# Step 2: os.getenv()   → reads from that memory
# If reversed → os.getenv() returns None because
# .env hasn't been loaded yet!
load_dotenv()


# ────────────────────────────────────────
# SHARED LLM INSTANCE
# ────────────────────────────────────────

# We create ONE LLM instance shared by ALL agents
# Think of it like this:
# Same human brain → different job training
# Doctor and Lawyer both have same brain type
# but trained completely differently!
# Same LLM → different role+goal+backstory = different behaviour!

llm = LLM(
    # groq/ prefix → tells CrewAI to use Groq as provider
    # llama-3.3-70b-versatile → current active Groq model
    #
    # ⚠️ IMPORTANT: If you get "model decommissioned" error
    # Go to: console.groq.com/docs/deprecations
    # and update this model name to the latest one!
    model="groq/llama-3.3-70b-versatile",

    # Read API key from .env file
    # NEVER hardcode API keys directly in code!
    # Why? If you push to GitHub → key gets exposed!
    # .env is in .gitignore so it stays private and safe
    api_key=os.getenv("GROQ_API_KEY"),

    # Temperature controls how creative vs focused the LLM is
    # 0.0 = completely deterministic, always same answer
    # 0.1 = very focused and factual (BEST for news!)
    # 0.7 = balanced creativity and accuracy
    # 1.0 = very creative and random (bad for news facts!)
    # We use 0.1 because news must be accurate not creative!
    temperature=0.1
)