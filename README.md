# 🎬 Agentic Research Studio

<p align="center">
  <strong>An autonomous 4-agent cognitive research studio powered by Groq LPU silicon, LangChain, and Tavily.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Groq-LPU%20Accelerated-E50914?style=for-the-badge&logo=groq&logoColor=white" alt="Groq">
  <img src="https://img.shields.io/badge/LangChain-Framework-black?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/Streamlit-Cinematic%20UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

## 🌟 Overview

**Agentic Research Studio** is a multi-agent system designed to research any topic on the web autonomously. Instead of relying on a single prompt or LLM query, it deploys a collaborative mesh of specialized AI agents that execute reconnaissance, scrape raw source articles, synthesize executive briefings, and perform adversarial critical auditing in real time.

All inference is accelerated via **Groq Cloud LPU™**, delivering ultra-low latency response times.

---

## 🧠 Multi-Agent Architecture

```
[ User Query ]
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ 🛰️ Stage 1: Radar Searcher Agent (Tavily Discovery)        │
│    • Formulates dynamic web search queries                  │
│    • Gathers top-ranking verifiable sources & links         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 📖 Stage 2: Deep Reader Agent (Multi-Strategy Extraction)   │
│    • Evaluates discovered links & selects highest-signal URL│
│    • Scrapes structured article text via Trafilatura        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ ✍️ Stage 3: Lead Author Agent (Groq Synthesis)             │
│    • Cross-references web snippets with full scraped text   │
│    • Generates publication-ready executive briefing         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 🧐 Stage 4: Senior Auditor Agent (Adversarial Critique)     │
│    • Audits report factual soundness, clarity & citations   │
│    • Delivers rigorous scorecard (X/10) + final verdict     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
[ 🎬 Premiere Deliverable: Executive Briefing + Scorecard ]
```

---

## ✨ Features

- **⚡ Groq LPU™ Acceleration**: Powered by high-throughput models like `openai/gpt-oss-120b` and `qwen/qwen3.8-27b`.
- **🎬 Netflix-Inspired Cinematic Studio**: Sleek obsidian and crimson interface with high-contrast typography, live pulsing beacons, and instant trending search chips.
- **📡 Synchronized Real-Time War Room**: Watch agent thoughts, decisions, tool calls, and extracted intelligence update live as each step executes.
- **📄 Robust Multi-Strategy Web Scraper**: Built-in fallback pipeline (`Trafilatura` ➔ `Readability-lxml` ➔ `BeautifulSoup`) to reliably extract clean article content without clutter.
- **📊 Adversarial Peer Review**: Automatic critical evaluation scoring the research from 1 to 10 with key strengths, warnings, and an auditor verdict.
- **⬇️ 1-Click Markdown Export**: Download complete executive briefings directly to `.md` for easy sharing.

---

## 📁 Repository Structure

```
agentic-research-studio/
├── src/
│   ├── agents/
│   │   └── agents.py       # Groq agent definitions & prompt chains
│   ├── pipelines/
│   │   └── pipeline.py     # End-to-end multi-agent execution pipeline
│   └── tools/
│       └── tools.py        # Tavily search & web scraping tools
├── app.py                  # Streamlit cinematic research studio UI
├── main.py                 # CLI entry point for headless execution
├── requirements.txt        # Project dependencies
├── .env.example            # Template for required environment variables
└── README.md               # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/taosiff/agentic-research-studio.git
cd agentic-research-studio
```

### 2. Create and Activate a Virtual Environment
```bash
# On Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

Edit `.env`:
```env
TAVILY_API_KEY="your-tavily-api-key"
GROQ_API_KEY="your-groq-api-key"
GROQ_MODEL="openai/gpt-oss-120b"
```

> **API Key Resources:**
> - [Get a Groq API Key (Free)](https://console.groq.com/keys)
> - [Get a Tavily Search API Key (Free)](https://app.tavily.com)

---

## 🖥️ Running the Application

### Launch the Web Studio (Streamlit)
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to access the studio.

### Run in Headless CLI Mode
```bash
python main.py
```

---

## ⚙️ Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq Cloud API Key for high-speed LLM inference | **Yes** |
| `TAVILY_API_KEY` | Tavily Search API Key for live web reconnaissance | **Yes** |
| `GROQ_MODEL` | Default model architecture (default: `openai/gpt-oss-120b`) | No |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
