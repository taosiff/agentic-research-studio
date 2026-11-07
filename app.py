import streamlit as st
import time
import os
import re
from dotenv import load_dotenv

load_dotenv()

from src.agents.agents import (
    get_groq_llm,
    execute_search_agent,
    execute_reader_agent,
    build_writer_chain,
    build_critic_chain,
)

st.set_page_config(
    page_title="Agentic Research Studio | Autonomous Multi-Agent Mesh",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --netflix-red: #E50914;
    --netflix-red-hover: #f40612;
    --netflix-red-glow: rgba(229, 9, 20, 0.45);
    --bg-dark: #0f1016;
    --card-surface: #171822;
    --card-border: rgba(255, 255, 255, 0.08);
    --text-pure: #ffffff;
    --text-muted: #9ca3af;
    --text-faint: #6b7280;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    color: var(--text-pure);
    background-color: var(--bg-dark);
}

.stApp {
    background-color: var(--bg-dark);
    background-image: 
        radial-gradient(circle at 50% 0%, rgba(229, 9, 20, 0.14) 0%, transparent 60%),
        radial-gradient(circle at 100% 100%, rgba(99, 102, 241, 0.08) 0%, transparent 45%),
        linear-gradient(180deg, #0b0c11 0%, #11131c 100%);
    background-attachment: fixed;
}

#MainMenu, header, footer { visibility: hidden !important; }
.block-container {
    padding: 1.5rem 3rem 4rem !important;
    max-width: 1400px !important;
}

.cinema-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.9rem 1.8rem;
    background: rgba(18, 19, 28, 0.85);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    backdrop-filter: blur(25px);
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.nav-logo {
    background: var(--netflix-red);
    color: #fff;
    font-weight: 900;
    font-size: 1.1rem;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    letter-spacing: -0.05em;
    box-shadow: 0 0 18px var(--netflix-red-glow);
}

.nav-title {
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    color: #ffffff;
}

.nav-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
    font-weight: 400;
}

.engine-pill {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    background: rgba(229, 9, 20, 0.12);
    border: 1px solid rgba(229, 9, 20, 0.35);
    padding: 0.35rem 0.9rem;
    border-radius: 100px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #ff4d58;
    font-weight: 600;
    letter-spacing: 0.05em;
}

.live-beacon {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #ff4d58;
    box-shadow: 0 0 12px #ff4d58;
    animation: beacon 1.8s infinite;
}

@keyframes beacon {
    0%, 100% { opacity: 0.4; transform: scale(0.9); }
    50% { opacity: 1; transform: scale(1.3); }
}

.hero-box {
    text-align: center;
    max-width: 820px;
    margin: 0 auto 2.2rem;
}

.hero-heading {
    font-size: clamp(2.2rem, 4vw, 3.4rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.6rem;
    color: #ffffff;
    line-height: 1.15;
}

.hero-highlight {
    background: linear-gradient(135deg, #ffffff 30%, #ff4d58 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 1.05rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 1.8rem;
    font-weight: 300;
}

.stTextInput > div > div > input {
    background: #14151f !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-size: 1.05rem !important;
    padding: 0.95rem 1.4rem !important;
    transition: all 0.25s ease !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.4) !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--netflix-red) !important;
    box-shadow: 0 0 0 3px rgba(229, 9, 20, 0.25), inset 0 2px 4px rgba(0,0,0,0.4) !important;
    background: #181926 !important;
}

.stButton > button {
    background: var(--netflix-red) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.02rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.9rem 2.2rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 8px 24px rgba(229, 9, 20, 0.35) !important;
    width: 100%;
}

.stButton > button:hover {
    background: var(--netflix-red-hover) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(229, 9, 20, 0.5) !important;
}

.trending-header {
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-faint);
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.agent-card {
    background: #151622;
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

.agent-card.running {
    border-color: var(--netflix-red);
    background: linear-gradient(180deg, rgba(229, 9, 20, 0.12) 0%, #151622 100%);
    box-shadow: 0 0 30px rgba(229, 9, 20, 0.35);
    animation: pulse-glow 2s infinite alternate;
}

@keyframes pulse-glow {
    0% { border-color: rgba(229, 9, 20, 0.4); }
    100% { border-color: rgba(229, 9, 20, 0.9); }
}

.agent-card.completed {
    border-color: rgba(16, 185, 129, 0.35);
    background: #151622;
}

.agent-top-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
}

.agent-identity {
    display: flex;
    align-items: center;
    gap: 0.65rem;
}

.agent-avatar {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: #202232;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
}

.agent-name {
    font-weight: 700;
    font-size: 0.95rem;
    color: #ffffff;
}

.agent-stage-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    background: rgba(255,255,255,0.06);
    color: var(--text-muted);
}

.agent-badge-active {
    background: rgba(229, 9, 20, 0.25) !important;
    color: #ff6b75 !important;
    border: 1px solid rgba(229, 9, 20, 0.5);
}

.agent-badge-done {
    background: rgba(16, 185, 129, 0.15) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.live-spinner-line {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-top: 0.5rem;
    padding: 0.5rem 0.8rem;
    background: rgba(229, 9, 20, 0.08);
    border-radius: 8px;
    border: 1px solid rgba(229, 9, 20, 0.2);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #ff6b75;
}

.radar-dots {
    display: inline-block;
    width: 14px;
    height: 14px;
    border: 2px solid #ff4d58;
    border-top-color: transparent;
    border-radius: 50%;
    animation: spin-radar 0.8s linear infinite;
}

@keyframes spin-radar {
    to { transform: rotate(360deg); }
}

.agent-thought-bubble {
    background: #0d0e15;
    border-left: 3px solid var(--netflix-red);
    border-radius: 0 8px 8px 0;
    padding: 0.65rem 0.9rem;
    margin: 0.6rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #cbd5e1;
    line-height: 1.5;
}

.agent-content-preview {
    font-size: 0.85rem;
    line-height: 1.55;
    color: var(--text-muted);
    max-height: 180px;
    overflow-y: auto;
    padding-right: 0.4rem;
}

.url-pill {
    display: inline-block;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 6px;
    padding: 0.2rem 0.5rem;
    font-size: 0.72rem;
    color: #38bdf8;
    text-decoration: none;
    margin: 0.2rem 0.2rem 0 0;
}

.premiere-card {
    background: #171825;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2.2rem;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
    position: relative;
}

.premiere-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 1.2rem;
    margin-bottom: 1.5rem;
}

.premiere-badge {
    background: linear-gradient(135deg, var(--netflix-red), #b91c1c);
    color: #fff;
    font-weight: 800;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    padding: 0.25rem 0.75rem;
    border-radius: 100px;
    text-transform: uppercase;
}

.scorecard-banner {
    background: linear-gradient(135deg, rgba(229, 9, 20, 0.12) 0%, rgba(30, 41, 59, 0.5) 100%);
    border: 1px solid rgba(229, 9, 20, 0.25);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.6rem;
}

.report-prose {
    font-size: 1.02rem;
    line-height: 1.85;
    color: #e2e8f0;
}

.report-prose h1, .report-prose h2, .report-prose h3 {
    color: #ffffff;
    font-weight: 700;
    letter-spacing: -0.02em;
}

.report-prose h1 { font-size: 1.75rem; margin-top: 1.4rem; margin-bottom: 0.8rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem; }
.report-prose h2 { font-size: 1.35rem; margin-top: 1.4rem; color: #ff6b75; }
.report-prose h3 { font-size: 1.15rem; margin-top: 1rem; color: #38bdf8; }
.report-prose ul { margin-left: 1.2rem; margin-bottom: 1rem; }
.report-prose li { margin-bottom: 0.4rem; }

.screen-standby {
    height: 480px;
    border: 2px dashed rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    background: rgba(18, 19, 28, 0.4);
}

.screen-working {
    height: 480px;
    border: 1px solid rgba(229, 9, 20, 0.4);
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2.5rem;
    background: linear-gradient(180deg, rgba(229, 9, 20, 0.08) 0%, rgba(18, 19, 28, 0.95) 100%);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.big-radar-pulse {
    width: 64px;
    height: 64px;
    border: 3px solid rgba(229, 9, 20, 0.2);
    border-top: 3px solid var(--netflix-red);
    border-radius: 50%;
    animation: spin-radar 1s linear infinite;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

if "pipeline_data" not in st.session_state:
    st.session_state.pipeline_data = {}
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

st.markdown("""
<div class="cinema-nav">
    <div class="nav-brand">
        <div class="nav-logo">ARS</div>
        <div>
            <div class="nav-title">AGENTIC RESEARCH STUDIO</div>
            <div class="nav-subtitle">Live Autonomous Intelligence & Critical Auditing</div>
        </div>
    </div>
    <div class="engine-pill">
        <div class="live-beacon"></div>
        <span>GROQ LPU™ ACCELERATED · 120B ENGINE</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="hero-heading">Autonomous Intelligence, <span class="hero-highlight">Live on Stage.</span></div>
    <div class="hero-sub">
        Deploy a 4-agent cognitive mesh powered by Groq LPU inference. Watch each agent think, 
        scrape, synthesize, and audit in synchronized real-time.
    </div>
</div>
""", unsafe_allow_html=True)

search_col, btn_col = st.columns([4.2, 1.2])

with search_col:
    user_topic = st.text_input(
        "Investigation Topic",
        value=st.session_state.topic_input,
        placeholder="Enter any topic (e.g. Next-Generation Solid-State Battery Breakthroughs in 2026)",
        key="topic_field",
        label_visibility="collapsed"
    )

with btn_col:
    start_btn = st.button("▶ Start Mission", use_container_width=True)

st.markdown('<div class="trending-header">🔥 Trending Investigations (Click to Explore):</div>', unsafe_allow_html=True)

def trigger_topic(chosen_topic: str):
    st.session_state.topic_input = chosen_topic
    st.session_state["topic_field"] = chosen_topic
    st.session_state.pipeline_data = {}
    st.session_state.is_running = True
    st.rerun()

t1, t2, t3, t4 = st.columns(4)
with t1:
    if st.button("🤖 Autonomous Agents in 2026", use_container_width=True):
        trigger_topic("Future of Autonomous Agentic AI Frameworks in 2026")
with t2:
    if st.button("⚡ Groq LPU vs NVIDIA GPUs", use_container_width=True):
        trigger_topic("Groq LPU vs Traditional NVIDIA GPUs for AI Inference")
with t3:
    if st.button("🧠 The Roadmap to AGI", use_container_width=True):
        trigger_topic("Scientific and Technical Milestones Required for AGI by 2030")
with t4:
    if st.button("🛡️ Post-Quantum Security", use_container_width=True):
        trigger_topic("Implementation of Post-Quantum Cryptography in Cloud Infrastructure")

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

if start_btn:
    active_query = user_topic.strip()
    if not active_query:
        st.warning("⚠️ Please specify a research topic to deploy the agents.")
    else:
        st.session_state.topic_input = active_query
        st.session_state.pipeline_data = {}
        st.session_state.is_running = True
        st.rerun()

col_warroom, col_premiere = st.columns([1.1, 1.3], gap="large")

with col_warroom:
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;">
        <div style="font-weight:800;font-size:1.15rem;letter-spacing:-0.02em;color:#fff;">
            📡 Live Agent War Room
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#9ca3af;">
            SYNCHRONIZED FEED
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    agent1_box = st.empty()
    agent2_box = st.empty()
    agent3_box = st.empty()
    agent4_box = st.empty()

with col_premiere:
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;">
        <div style="font-weight:800;font-size:1.15rem;letter-spacing:-0.02em;color:#fff;">
            🎬 Premiere Deliverable
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#9ca3af;">
            INTELLIGENCE BRIEFING
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    premiere_screen = st.empty()

if st.session_state.is_running:
    topic_query = st.session_state.topic_input
    groq_llm = get_groq_llm()
    data = {}

    premiere_screen.markdown(f"""
    <div class="screen-working">
        <div class="big-radar-pulse"></div>
        <div style="font-size:1.35rem;font-weight:700;color:#fff;margin-bottom:0.5rem;">
            Autonomous Mesh Active
        </div>
        <div style="font-size:0.88rem;color:#ff6b75;font-family:'JetBrains Mono',monospace;margin-bottom:1rem;">
            STAGE 1/4: Scouring web intelligence on Tavily...
        </div>
        <div style="font-size:0.82rem;color:#9ca3af;max-width:420px;line-height:1.5;">
            Investigating: <span style="color:#ffffff;">"{topic_query}"</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    agent1_box.markdown(f"""
    <div class="agent-card running">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">🛰️</div>
                <div class="agent-name">Agent 01: Radar Searcher</div>
            </div>
            <div class="agent-stage-badge agent-badge-active">● DISPATCHING TAVILY</div>
        </div>
        <div class="agent-thought-bubble">
            🧠 <b>Thinking:</b> Analyzing topic: "{topic_query}". Formulating high-signal search queries and dispatching Tavily live reconnaissance...
        </div>
        <div class="live-spinner-line">
            <div class="radar-dots"></div>
            <span>Scanning live web index & ranking verified sources...</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    search_data = execute_search_agent(topic_query, custom_llm=groq_llm)
    data["search"] = search_data["summary"]
    data["search_raw"] = search_data["raw"]
    
    urls_found = re.findall(r'https?://[^\s\)]+', search_data["raw"])[:4]
    url_pills_html = "".join([f'<a href="{u}" target="_blank" class="url-pill">🔗 {u.split("/")[2]}</a>' for u in urls_found])
    
    agent1_box.markdown(f"""
    <div class="agent-card completed">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">🛰️</div>
                <div class="agent-name">Agent 01: Radar Searcher</div>
            </div>
            <div class="agent-stage-badge agent-badge-done">✔ DISCOVERY COMPLETE</div>
        </div>
        <div class="agent-thought-bubble">
            ⚡ <b>Action:</b> Discovered {len(urls_found)} verified intelligence sources via query: <i>"{search_data['query']}"</i>
        </div>
        <div style="margin-top:0.4rem;">{url_pills_html}</div>
    </div>
    """, unsafe_allow_html=True)

    premiere_screen.markdown(f"""
    <div class="screen-working">
        <div class="big-radar-pulse"></div>
        <div style="font-size:1.35rem;font-weight:700;color:#fff;margin-bottom:0.5rem;">
            Deep Content Reader Ingesting
        </div>
        <div style="font-size:0.88rem;color:#ff6b75;font-family:'JetBrains Mono',monospace;margin-bottom:1rem;">
            STAGE 2/4: Scraping primary article & filtering noise...
        </div>
        <div style="font-size:0.82rem;color:#9ca3af;max-width:420px;line-height:1.5;">
            Analyzing primary source citations...
        </div>
    </div>
    """, unsafe_allow_html=True)

    agent2_box.markdown(f"""
    <div class="agent-card running">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">📖</div>
                <div class="agent-name">Agent 02: Deep Content Reader</div>
            </div>
            <div class="agent-stage-badge agent-badge-active">● SCRAPING ARTICLE</div>
        </div>
        <div class="agent-thought-bubble">
            🧠 <b>Thinking:</b> Selecting the most authoritative target URL and running Trafilatura multi-strategy scraper...
        </div>
        <div class="live-spinner-line">
            <div class="radar-dots"></div>
            <span>Fetching full document & stripping boilerplate...</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    reader_data = execute_reader_agent(topic_query, search_data["raw"], custom_llm=groq_llm)
    data["reader"] = reader_data["content"]
    data["scraped_url"] = reader_data["url"]
    
    agent2_box.markdown(f"""
    <div class="agent-card completed">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">📖</div>
                <div class="agent-name">Agent 02: Deep Content Reader</div>
            </div>
            <div class="agent-stage-badge agent-badge-done">✔ EXTRACTION COMPLETE</div>
        </div>
        <div class="agent-thought-bubble">
            ⚡ <b>Action:</b> Extracted {len(reader_data['content'])} characters from <code>{reader_data['url'][:45]}...</code>
        </div>
        <div class="agent-content-preview">
            {reader_data['content'][:260]}...
        </div>
    </div>
    """, unsafe_allow_html=True)

    premiere_screen.markdown(f"""
    <div class="screen-working">
        <div class="big-radar-pulse"></div>
        <div style="font-size:1.35rem;font-weight:700;color:#fff;margin-bottom:0.5rem;">
            Lead Synthesis Author Active
        </div>
        <div style="font-size:0.88rem;color:#ff6b75;font-family:'JetBrains Mono',monospace;margin-bottom:1rem;">
            STAGE 3/4: Groq LPU silicon formulating executive briefing...
        </div>
        <div style="font-size:0.82rem;color:#9ca3af;max-width:420px;line-height:1.5;">
            Cross-referencing web discovery with deep scraped intelligence...
        </div>
    </div>
    """, unsafe_allow_html=True)

    agent3_box.markdown(f"""
    <div class="agent-card running">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">✍️</div>
                <div class="agent-name">Agent 03: Lead Synthesis Author</div>
            </div>
            <div class="agent-stage-badge agent-badge-active">● SYNTHESIZING REPORT</div>
        </div>
        <div class="agent-thought-bubble">
            🧠 <b>Thinking:</b> Generating structured executive briefing on Groq LPU silicon...
        </div>
        <div class="live-spinner-line">
            <div class="radar-dots"></div>
            <span>Formulating executive analysis, implications & outlook...</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    writer_chain_inst = build_writer_chain(custom_llm=groq_llm)
    research_payload = (
        f"SEARCH RESULTS:\n{data['search']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{data['reader']}"
    )
    raw_report = writer_chain_inst.invoke({
        "topic": topic_query,
        "research": research_payload
    })
    data["writer"] = raw_report
    
    agent3_box.markdown(f"""
    <div class="agent-card completed">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">✍️</div>
                <div class="agent-name">Agent 03: Lead Synthesis Author</div>
            </div>
            <div class="agent-stage-badge agent-badge-done">✔ REPORT DRAFTED</div>
        </div>
        <div class="agent-thought-bubble">
            ⚡ <b>Action:</b> Synthesized comprehensive executive briefing ({len(raw_report.split())} words).
        </div>
    </div>
    """, unsafe_allow_html=True)

    premiere_screen.markdown(f"""
    <div class="screen-working">
        <div class="big-radar-pulse"></div>
        <div style="font-size:1.35rem;font-weight:700;color:#fff;margin-bottom:0.5rem;">
            Senior Auditor Auditing
        </div>
        <div style="font-size:0.88rem;color:#ff6b75;font-family:'JetBrains Mono',monospace;margin-bottom:1rem;">
            STAGE 4/4: Evaluating factual rigor & generating scorecard...
        </div>
        <div style="font-size:0.82rem;color:#9ca3af;max-width:420px;line-height:1.5;">
            Executing adversarial peer review...
        </div>
    </div>
    """, unsafe_allow_html=True)

    agent4_box.markdown(f"""
    <div class="agent-card running">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">🧐</div>
                <div class="agent-name">Agent 04: Senior Research Auditor</div>
            </div>
            <div class="agent-stage-badge agent-badge-active">● AUDITING QUALITY</div>
        </div>
        <div class="agent-thought-bubble">
            🧠 <b>Thinking:</b> Performing adversarial review. Checking factual rigor, citations, coverage, and computing overall scorecard...
        </div>
        <div class="live-spinner-line">
            <div class="radar-dots"></div>
            <span>Scoring publication readiness & verifying citations...</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    critic_chain_inst = build_critic_chain(custom_llm=groq_llm)
    raw_critic = critic_chain_inst.invoke({
        "report": data["writer"]
    })
    data["critic"] = raw_critic
    
    agent4_box.markdown(f"""
    <div class="agent-card completed">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">🧐</div>
                <div class="agent-name">Agent 04: Senior Research Auditor</div>
            </div>
            <div class="agent-stage-badge agent-badge-done">✔ AUDIT FINALIZED</div>
        </div>
        <div class="agent-thought-bubble">
            ⚡ <b>Action:</b> Factual verification and score completed.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.pipeline_data = data
    st.session_state.is_running = False
    st.rerun()

d = st.session_state.pipeline_data

if d and "writer" in d:
    urls_found = re.findall(r'https?://[^\s\)]+', d.get("search_raw", d.get("search", "")))[:4]
    url_pills_html = "".join([f'<a href="{u}" target="_blank" class="url-pill">🔗 {u.split("/")[2]}</a>' for u in urls_found])
    agent1_box.markdown(f"""
    <div class="agent-card completed">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">🛰️</div>
                <div class="agent-name">Agent 01: Radar Searcher</div>
            </div>
            <div class="agent-stage-badge agent-badge-done">✔ DISCOVERY COMPLETE</div>
        </div>
        <div class="agent-thought-bubble">
            ⚡ <b>Action:</b> Scanned web and isolated {len(urls_found)} high-impact intelligence sources.
        </div>
        <div style="margin-top:0.4rem;">{url_pills_html}</div>
    </div>
    """, unsafe_allow_html=True)

    raw_scrape = d.get("reader", "")
    scraped_url = d.get("scraped_url", "")
    url_tag = f"from <code>{scraped_url[:40]}...</code>" if scraped_url else ""
    agent2_box.markdown(f"""
    <div class="agent-card completed">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">📖</div>
                <div class="agent-name">Agent 02: Deep Content Reader</div>
            </div>
            <div class="agent-stage-badge agent-badge-done">✔ EXTRACTION COMPLETE</div>
        </div>
        <div class="agent-thought-bubble">
            ⚡ <b>Action:</b> Scraped deep article payload ({len(raw_scrape)} characters) {url_tag}.
        </div>
        <div class="agent-content-preview">
            {raw_scrape[:260]}...
        </div>
    </div>
    """, unsafe_allow_html=True)

    raw_report = d.get("writer", "")
    agent3_box.markdown(f"""
    <div class="agent-card completed">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">✍️</div>
                <div class="agent-name">Agent 03: Lead Synthesis Author</div>
            </div>
            <div class="agent-stage-badge agent-badge-done">✔ REPORT DRAFTED</div>
        </div>
        <div class="agent-thought-bubble">
            ⚡ <b>Action:</b> Formulated structured briefing ({len(raw_report.split())} words) on Groq LPU silicon.
        </div>
    </div>
    """, unsafe_allow_html=True)

    agent4_box.markdown(f"""
    <div class="agent-card completed">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">🧐</div>
                <div class="agent-name">Agent 04: Senior Research Auditor</div>
            </div>
            <div class="agent-stage-badge agent-badge-done">✔ AUDIT FINALIZED</div>
        </div>
        <div class="agent-thought-bubble">
            ⚡ <b>Action:</b> Verified factual rigor, citations, and critical quality rating.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with premiere_screen.container():
        st.markdown('<div class="premiere-card">', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="premiere-banner">
            <div>
                <span class="premiere-badge">PREMIERE RELEASE</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#9ca3af;margin-left:0.8rem;">
                    TOPIC: {st.session_state.topic_input[:50]}...
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_dl, col_blank = st.columns([1.5, 4.5])
        with col_dl:
            st.download_button(
                label="⬇ Export Report (.md)",
                data=d["writer"],
                file_name=f"agentic_research_brief_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        if "critic" in d:
            st.markdown(f"""
            <div class="scorecard-banner">
                {d["critic"]}
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('<div class="report-prose">', unsafe_allow_html=True)
        st.markdown(d["writer"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    agent1_box.markdown("""
    <div class="agent-card">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">🛰️</div>
                <div class="agent-name">Agent 01: Radar Searcher</div>
            </div>
            <div class="agent-stage-badge">STANDBY</div>
        </div>
        <div style="font-size:0.82rem;color:#6b7280;">Awaiting mission launch to conduct web intelligence discovery.</div>
    </div>
    """, unsafe_allow_html=True)
    
    agent2_box.markdown("""
    <div class="agent-card">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">📖</div>
                <div class="agent-name">Agent 02: Deep Content Reader</div>
            </div>
            <div class="agent-stage-badge">STANDBY</div>
        </div>
        <div style="font-size:0.82rem;color:#6b7280;">Ready to inspect and scrape primary source documentation.</div>
    </div>
    """, unsafe_allow_html=True)

    agent3_box.markdown("""
    <div class="agent-card">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">✍️</div>
                <div class="agent-name">Agent 03: Lead Synthesis Author</div>
            </div>
            <div class="agent-stage-badge">STANDBY</div>
        </div>
        <div style="font-size:0.82rem;color:#6b7280;">Ready to synthesize multi-source data into an executive brief.</div>
    </div>
    """, unsafe_allow_html=True)

    agent4_box.markdown("""
    <div class="agent-card">
        <div class="agent-top-row">
            <div class="agent-identity">
                <div class="agent-avatar">🧐</div>
                <div class="agent-name">Agent 04: Senior Research Auditor</div>
            </div>
            <div class="agent-stage-badge">STANDBY</div>
        </div>
        <div style="font-size:0.82rem;color:#6b7280;">Ready to evaluate factual rigor and issue peer review scorecard.</div>
    </div>
    """, unsafe_allow_html=True)

    premiere_screen.markdown("""
    <div class="screen-standby">
        <div style="font-size:3.5rem;margin-bottom:1rem;color:#ff4d58;">🎬</div>
        <div style="font-size:1.4rem;font-weight:700;color:#fff;margin-bottom:0.5rem;">
            Agent Studio Ready for Investigation
        </div>
        <div style="font-size:0.92rem;color:#9ca3af;max-width:440px;line-height:1.6;">
            Choose a trending investigation above or type any topic in the search bar. 
            The 4-agent mesh will initiate live and present the executive deliverable here.
        </div>
    </div>
    """, unsafe_allow_html=True)
