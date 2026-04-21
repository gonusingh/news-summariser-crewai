# 🗞️ Morning News Summariser — AI Agentic System

> **An intelligent multi-agent news summariser built with CrewAI and Groq LLM**
> Built by **Vinit Kumar** | TCS Software Developer | Heritage Institute of Technology, Kolkata

---

## 📌 What is this project?

This is an **Agentic AI** application that automatically:
1. Searches the internet for today's top news
2. Filters only relevant stories (AI, Tech, Global Affairs, Science)
3. Writes a clean friendly morning briefing
4. Fact-checks every story has a real source URL

All of this happens **automatically** — you just run one command every morning!

---

## 🤖 What is Agentic AI?

Normal AI answers questions by following **fixed steps**.

**Agentic AI** works like a smart employee:
- Receives a **goal** (not just a question)
- **Decides its own steps** to achieve that goal
- Uses **tools** (search, browser, etc.) to get things done
- **Loops until** the desired outcome is achieved

This project uses **4 AI agents working as a team** — just like a real newsroom!

---

## 🏗️ Architecture — How it works

```
USER runs: python main.py
                │
                ▼
        ┌───────────────┐
        │   main.py     │  ← Entry point, starts the crew
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │   crew.py     │  ← Assembles all agents + tasks
        └───────┬───────┘
                │
                ▼
    ┌───────────────────────┐
    │   SEQUENTIAL PROCESS  │
    │                       │
    │  Agent 1 (Collector)  │  → Searches internet for news
    │         ↓             │
    │  Agent 2 (Filter)     │  → Picks most relevant stories
    │         ↓             │
    │  Agent 3 (Summariser) │  → Writes morning briefing
    │         ↓             │
    │  Agent 4 (Fact Check) │  → Verifies every URL is real
    └───────────────────────┘
                │
                ▼
    🌞 YOUR MORNING NEWS BRIEFING!
```

---

## 👥 The 4 Agents — Meet your AI team!

### Agent 1 — News Collector 🔍
| Property | Value |
|----------|-------|
| Role | Senior News Research Journalist |
| Job | Search internet for today's top 5 news |
| Tools | DuckDuckGo Search Tool |
| Input | Nothing — starts fresh every morning |
| Output | Raw headlines + URLs + summaries |

### Agent 2 — News Filter ✂️
| Property | Value |
|----------|-------|
| Role | Senior News Editor |
| Job | Pick only relevant and important stories |
| Tools | None — uses LLM brain only |
| Input | Raw news from Agent 1 (via context) |
| Output | Top 3-5 filtered relevant stories |

### Agent 3 — News Summariser ✍️
| Property | Value |
|----------|-------|
| Role | Morning Newsletter Writer |
| Job | Write clean friendly morning briefing |
| Tools | None — pure writing task |
| Input | Filtered news from Agent 2 (via context) |
| Output | Beautiful formatted morning summary |

### Agent 4 — Fact Checker ✅
| Property | Value |
|----------|-------|
| Role | News Fact Verification Journalist |
| Job | Verify every story has a real source URL |
| Tools | DuckDuckGo Search Tool |
| Input | Summary from Agent 3 (via context) |
| Output | Final verified news briefing |

---

## 🧠 Core Concepts Used

### ReAct Pattern (Reason + Act)
Every agent thinks like this:
```
REASON → "What do I need to do?"
ACT    → Uses a tool
REASON → "Was that enough?"
ACT    → Uses another tool or stops
LOOP   → Until task is complete!
```

### Context Passing
Agents pass information to each other:
```
Agent 1 output → becomes Agent 2 input
Agent 2 output → becomes Agent 3 input
Agent 3 output → becomes Agent 4 input
```

### Sequential Process
Tasks run one after another:
```
Task 1 finishes → Task 2 starts → Task 3 starts → Task 4 starts
```

### Hallucination Prevention
Agent 4 (Fact Checker) searches every story online.
**No URL found = Story removed from final output!**
This protects readers from fake news.

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Agent Framework | CrewAI | Manages multi-agent teams |
| LLM Brain | Groq (Llama 3.3 70B) | Free, fast, powerful |
| Search Tool | DuckDuckGo (ddgs) | Free, no API key needed |
| Environment | python-dotenv | Secure API key management |
| LLM Bridge | LiteLLM | Connects CrewAI to Groq |

---

## 📁 Project Structure

```
news_summariser/
│
├── .env                 → API keys (NEVER share this!)
├── requirements.txt     → All Python dependencies
│
├── agents.py            → Defines all 4 AI agents
│                          (roles, goals, backstories, tools)
│
├── tasks.py             → Defines all 4 tasks
│                          (descriptions, expected outputs)
│
├── crew.py              → Assembles agents + tasks into crew
│                          (process, order, configuration)
│
└── main.py              → Entry point — run this every morning!
                           (kickoff, formatting, output)
```

---

## ⚙️ Setup Instructions

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/news_summariser.git
cd news_summariser
```

### Step 2 — Create virtual environment
```bash
# Create venv
python -m venv venv

# Activate on Windows PowerShell
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

> **Why venv?** Virtual environment keeps project dependencies isolated. Different projects need different package versions — venv prevents conflicts!

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Get your free Groq API key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign in with Google
3. Click **API Keys → Create API Key**
4. Copy the key (starts with `gsk_...`)

### Step 5 — Create .env file
```bash
# Create .env file
GROQ_API_KEY=gsk_your_actual_key_here
```

> ⚠️ **Never share your .env file or push it to GitHub!**

### Step 6 — Run the project!
```bash
python main.py
```

---

## 📊 Sample Output

```
==================================================
   🗞️  MORNING NEWS SUMMARISER
   📅  Tuesday, 21 April 2026
==================================================

🌞 Good morning, and welcome to your daily briefing.

🤖 Google challenges Nvidia with new chips to speed up AI
   Google's AI chips are giving Nvidia competition, changing
   the game for artificial intelligence technology.
   🔗 https://latimes.com/...

💼 Elon Musk has a solution for AI threat to jobs
   Universal high income proposal sparks global debate
   about work, meaning, and the future of employment.
   🔗 https://msn.com/...

📉 OpenAI loses multiple executives in leadership shakeup
   Three key OpenAI executives left in a single day,
   marking major changes at the AI startup before its IPO.
   🔗 https://cnbc.com/...

🎓 Record number of researchers run for office in US
   Scientists entering politics motivated by cuts to
   science funding and attacks on scientific evidence.
   🔗 https://nature.com/...

Stay informed, stay ahead, and make today count 🌟!
==================================================
```

---

## ⚠️ Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `model decommissioned` | Groq retired the model | Check [console.groq.com/docs/deprecations](https://console.groq.com/docs/deprecations) for current model |
| `Rate limit exceeded` | Too many tokens used | Wait 60 seconds and run again — Groq resets per minute |
| `403 Ratelimit` from DuckDuckGo | Too many searches too fast | `time.sleep(3)` already handles this — just retry |
| `ModuleNotFoundError` | Package not installed | Run `pip install -r requirements.txt` |
| `GROQ_API_KEY is None` | .env not loaded correctly | Make sure `load_dotenv()` is called before `os.getenv()` |
| `tool_use_failed` | LLM tool calling format issue | Add `use_system_prompt=False` to all agents |

---

## 🧩 Key Learning Concepts

### 1. What is an Agent?
An AI agent has:
- **Role** → job title (shapes identity)
- **Goal** → what it wants to achieve
- **Backstory** → experience prompt (shapes behaviour)
- **Tools** → superpowers it can use
- **LLM** → the brain it thinks with

### 2. What is a Tool?
A tool gives agents superpowers they don't naturally have.
LLMs cannot search the internet by default.
The `@tool` decorator converts a Python function into something agents can discover and call!

### 3. What is Context?
Context = output of previous task passed as input to next task.
This is how agents communicate with each other!

### 4. What is Hallucination?
When an LLM makes up information that doesn't exist.
Agent 4 (Fact Checker) prevents this by verifying every story has a real URL!

---

## 🚀 Future Improvements (Level 2)

- [ ] Add **CrewAI Flow** — detect crisis news and trigger breaking alert
- [ ] Add **LinkedIn Post Writer** agent — auto-post AI news summaries
- [ ] Add **Email Alert** agent — send briefing to your inbox daily
- [ ] Add **Memory** — remember user preferences across sessions
- [ ] Add **Streamlit UI** — beautiful web interface
- [ ] Schedule with **cron job** — auto-run every morning at 8am

---

## 👨‍💻 Author

**Vinit Kumar**
- 🏢 Software Developer at Tata Consultancy Services
- 🎓 B.Tech (ECE) — Heritage Institute of Technology, Kolkata
- 💼 [LinkedIn](https://www.linkedin.com/in/vinit7250)
- 📧 vinitsharma8521@gmail.com

---

## 📄 License

MIT License — free to use, modify and distribute.

---

## 🙏 Acknowledgements

- [CrewAI](https://docs.crewai.com) — Multi-agent framework
- [Groq](https://console.groq.com) — Free LLM API
- [DuckDuckGo Search](https://pypi.org/project/ddgs/) — Free news search
- Mentor **Aarush Sharma** — for guiding the agentic AI journey!