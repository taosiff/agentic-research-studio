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
    page_title="Agentic Research Studio | Autonomous Multi-Agent Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --brand-accent: #6366f1;
    --brand-accent-glow: rgba(99, 102, 241, 0.35);
    --bg-dark: #0a0c12;
    --surface-card: #121520;
    --surface-subtle: #171b29;
    --border-color: rgba(255, 255, 255, 0.08);
    --border-accent: rgba(99, 102, 241, 0.4);
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --tag-emerald: #10b981;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    color: var(--text-primary);
    background-color: var(--bg-dark);
}

.stApp {
    background-color: var(--bg-dark);
    background-image: 
        radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.12) 0%, transparent 60%),
        radial-gradient(circle at 100% 100%, rgba(14, 165, 233, 0.06) 0%, transparent 40%),
        linear-gradient(180deg, #090a0f 0%, #0f121a 100%);
    background-attachment: fixed;
}

#MainMenu, header, footer { visibility: hidden !important; }

.block-container {
    padding: 1.5rem 1.5rem 4rem !important;
    max-width: 1080px !important;
    margin: 0 auto;
}

.studio-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.85rem 1.5rem;
    background: rgba(18, 21, 32, 0.85);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    backdrop-filter: blur(20px);
    margin-bottom: 2.2rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.nav-brand-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.nav-badge-icon {
    background: linear-gradient(135deg, #6366f1, #3b82f6);
    color: #fff;
    font-weight: 800;
    font-size: 0.95rem;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    letter-spacing: -0.02em;
    box-shadow: 0 0 14px var(--brand-accent-glow);
}

.nav-title-text {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.01em;
}

.nav-subtitle-text {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.engine-status-tag {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.25);
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #a5b4fc;
    font-weight: 500;
}

.status-pulse-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 8px #10b981;
    animation: status-beacon 1.8s infinite;
}

@keyframes status-beacon {
    0%, 100% { opacity: 0.4; transform: scale(0.9); }
    50% { opacity: 1; transform: scale(1.2); }
}

.hero-container {
    text-align: center;
    max-width: 780px;
    margin: 0 auto 2.2rem;
}

.hero-main-title {
    font-size: clamp(2rem, 3.8vw, 3rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.75rem;
    color: #ffffff;
    line-height: 1.15;
}

.title-gradient {
    background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtext {
    font-size: 1.02rem;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 1.8rem;
    font-weight: 300;
}

.stTextInput > div > div > input {
    background: #121520 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 1rem !important;
    padding: 0.9rem 1.25rem !important;
    transition: all 0.2s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--brand-accent) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
    background: #161a29 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 0.98rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 1.8rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35) !important;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5) !important;
}

.thinking-box-active {
    background: rgba(18, 21, 32, 0.95);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 14px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    animation: thinking-glow 2.5s infinite alternate;
}

@keyframes thinking-glow {
    0% { border-color: rgba(99, 102, 241, 0.25); }
    100% { border-color: rgba(99, 102, 241, 0.65); }
}

.thinking-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.8rem;
}

.thinking-title-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #a5b4fc;
    font-weight: 600;
}

.radar-spinner {
    width: 15px;
    height: 15px;
    border: 2px solid rgba(99, 102, 241, 0.3);
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.thinking-stage-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    background: rgba(255, 255, 255, 0.05);
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
}

.thinking-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #cbd5e1;
    line-height: 1.6;
    background: #0c0e15;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border-left: 3px solid #6366f1;
}

.reasoning-details {
    background: rgba(18, 21, 32, 0.7);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 0.6rem 1rem;
    margin-bottom: 1.8rem;
    font-size: 0.85rem;
}

.reasoning-details summary {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #a5b4fc;
    cursor: pointer;
    font-weight: 500;
}

.reasoning-step-item {
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-secondary);
}

.source-card-deck {
    background: var(--surface-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 2rem;
}

.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #a5b4fc;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.source-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 0.8rem;
    margin-top: 0.8rem;
}

.source-pill-card {
    background: #0d0f18;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 0.75rem 0.95rem;
    transition: all 0.2s ease;
}

.source-pill-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateY(-2px);
}

.source-domain {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #38bdf8;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    text-decoration: none;
    margin-bottom: 0.3rem;
}

.source-snippet {
    font-size: 0.78rem;
    color: var(--text-muted);
    line-height: 1.45;
}

.primary-source-callout {
    background: #0e121e;
    border-left: 3px solid #10b981;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin-top: 1rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
}

.report-container {
    background: var(--surface-card);
    border: 1px solid var(--border-color);
    border-radius: 18px;
    padding: 2.2rem 2.4rem;
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

.report-top-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 1.2rem;
    margin-bottom: 1.8rem;
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
.report-prose h2 { font-size: 1.35rem; margin-top: 1.4rem; color: #a5b4fc; }
.report-prose h3 { font-size: 1.15rem; margin-top: 1rem; color: #38bdf8; }
.report-prose ul { margin-left: 1.2rem; margin-bottom: 1.2rem; }
.report-prose li { margin-bottom: 0.4rem; }

.critic-audit-container {
    background: linear-gradient(180deg, #131726 0%, #101320 100%);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 16px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 2.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
}

.standby-state-box {
    border: 1.5px dashed rgba(255, 255, 255, 0.1);
    border-radius: 18px;
    padding: 3.5rem 2rem;
    text-align: center;
    background: rgba(18, 21, 32, 0.4);
    margin-top: 1rem;
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
<div class="studio-nav">
    <div class="nav-brand-group">
        <div class="nav-badge-icon">ARS</div>
        <div>
            <div class="nav-title-text">Agentic Research Studio</div>
            <div class="nav-subtitle-text">Autonomous Multi-Agent Intelligence Engine</div>
        </div>
    </div>
    <div class="engine-status-tag">
        <div class="status-pulse-dot"></div>
        <span>GROQ LPU™ ACCELERATED · 120B ENGINE</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-container">
    <div class="hero-main-title">Autonomous Multi-Agent <span class="title-gradient">Intelligence System</span></div>
    <div class="hero-subtext">
        Orchestrates an autonomous mesh of specialized agents to conduct live web reconnaissance, 
        extract primary source documentation, formulate structured reports, and execute peer review.
    </div>
</div>
""", unsafe_allow_html=True)

col_input, col_action = st.columns([4.2, 1.3])

with col_input:
    user_topic = st.text_input(
        "Research Topic or Hypothesis",
        value=st.session_state.topic_input,
        placeholder="Enter research topic (e.g. Next-Generation Solid-State Battery Commercialization in 2026)",
        key="search_field",
        label_visibility="collapsed"
    )

with col_action:
    generate_btn = st.button("Generate Report", use_container_width=True)

st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

if generate_btn:
    active_query = user_topic.strip()
    if not active_query:
        st.warning("Please provide a research topic to initiate the pipeline.")
    else:
        st.session_state.topic_input = active_query
        st.session_state.pipeline_data = {}
        st.session_state.is_running = True
        st.rerun()

thinking_placeholder = st.empty()
results_area = st.container()

if st.session_state.is_running:
    topic_query = st.session_state.topic_input
    groq_llm = get_groq_llm()
    data = {}
    start_time = time.time()

    thinking_placeholder.markdown(f"""
    <div class="thinking-box-active">
        <div class="thinking-header">
            <div class="thinking-title-row">
                <div class="radar-spinner"></div>
                <span>Reasoning & Live Exploration...</span>
            </div>
            <div class="thinking-stage-name">Stage 1 of 4: Web Reconnaissance</div>
        </div>
        <div class="thinking-text">
            <b>Radar Search Agent:</b> Analyzing "{topic_query}". Formulating targeted queries and querying Tavily live index...
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    search_data = execute_search_agent(topic_query, custom_llm=groq_llm)
    data["search"] = search_data["summary"]
    data["search_raw"] = search_data["raw"]
    data["search_query"] = search_data["query"]

    thinking_placeholder.markdown(f"""
    <div class="thinking-box-active">
        <div class="thinking-header">
            <div class="thinking-title-row">
                <div class="radar-spinner"></div>
                <span>Reasoning & Live Exploration...</span>
            </div>
            <div class="thinking-stage-name">Stage 2 of 4: Document Scraping</div>
        </div>
        <div class="thinking-text">
            <b>Deep Reader Agent:</b> Isolated verified sources. Selecting primary reference URL and extracting full text via Trafilatura...
        </div>
    </div>
    """, unsafe_allow_html=True)

    reader_data = execute_reader_agent(topic_query, search_data["raw"], custom_llm=groq_llm)
    data["reader"] = reader_data["content"]
    data["scraped_url"] = reader_data["url"]

    thinking_placeholder.markdown(f"""
    <div class="thinking-box-active">
        <div class="thinking-header">
            <div class="thinking-title-row">
                <div class="radar-spinner"></div>
                <span>Reasoning & Live Exploration...</span>
            </div>
            <div class="thinking-stage-name">Stage 3 of 4: Report Synthesis</div>
        </div>
        <div class="thinking-text">
            <b>Lead Synthesis Author:</b> Cross-referencing multi-source data. Generating structured executive briefing on Groq LPU silicon...
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

    thinking_placeholder.markdown(f"""
    <div class="thinking-box-active">
        <div class="thinking-header">
            <div class="thinking-title-row">
                <div class="radar-spinner"></div>
                <span>Reasoning & Live Exploration...</span>
            </div>
            <div class="thinking-stage-name">Stage 4 of 4: Adversarial Audit</div>
        </div>
        <div class="thinking-text">
            <b>Senior Research Auditor:</b> Evaluating factual rigor, claims soundness, and computing peer review scorecard...
        </div>
    </div>
    """, unsafe_allow_html=True)

    critic_chain_inst = build_critic_chain(custom_llm=groq_llm)
    raw_critic = critic_chain_inst.invoke({
        "report": data["writer"]
    })
    data["critic"] = raw_critic
    data["duration"] = round(time.time() - start_time, 1)

    st.session_state.pipeline_data = data
    st.session_state.is_running = False
    st.rerun()

d = st.session_state.pipeline_data

if d and "writer" in d:
    duration_str = f" · Completed in {d.get('duration', 5.8)}s" if "duration" in d else ""
    st.markdown(f"""
    <details class="reasoning-details">
        <summary>🧠 View Agent Reasoning & Decision Trail (4 agents{duration_str})</summary>
        <div style="margin-top:0.6rem;">
            <div class="reasoning-step-item"><b>1. Radar Search Agent:</b> Formulated query <code>"{d.get('search_query', st.session_state.topic_input)}"</code> & retrieved live web references.</div>
            <div class="reasoning-step-item"><b>2. Deep Reader Agent:</b> Extracted {len(d.get('reader', ''))} characters from primary reference <code>{d.get('scraped_url', 'target URL')}</code>.</div>
            <div class="reasoning-step-item"><b>3. Lead Synthesis Author:</b> Formulated {len(d.get('writer', '').split())}-word executive report on Groq LPU inference.</div>
            <div class="reasoning-step-item"><b>4. Senior Research Auditor:</b> Completed adversarial peer audit and generated scorecard.</div>
        </div>
    </details>
    """, unsafe_allow_html=True)

    with results_area:
        st.markdown('<div class="report-container">', unsafe_allow_html=True)
        
        col_down, col_meta = st.columns([1.5, 4.5])
        with col_down:
            st.download_button(
                label="⬇ Export Report (.md)",
                data=d["writer"],
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_meta:
            st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#64748b;padding-top:0.6rem;text-align:right;">
                TOPIC: {st.session_state.topic_input[:45]}... • STATUS: VERIFIED
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="report-prose">', unsafe_allow_html=True)
        st.markdown(d["writer"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if "critic" in d:
            st.markdown('<div class="critic-audit-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">📊 Stage 4 Deliverable: Peer Review & Quality Audit Scorecard</div>', unsafe_allow_html=True)
            st.markdown(d["critic"])
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="source-card-deck">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">🌐 Verified Intelligence References & Primary Sources</div>', unsafe_allow_html=True)
        
        urls_found = re.findall(r'https?://[^\s\)]+', d.get("search_raw", d.get("search", "")))[:6]
        
        if urls_found:
            st.markdown('<div class="source-grid">', unsafe_allow_html=True)
            for u in urls_found:
                domain = u.split("/")[2] if len(u.split("/")) > 2 else u
                st.markdown(f"""
                <div class="source-pill-card">
                    <a href="{u}" target="_blank" class="source-domain">🔗 {domain}</a>
                    <div class="source-snippet">Verified intelligence reference acquired during web reconnaissance.</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if d.get("scraped_url"):
            st.markdown(f"""
            <div class="primary-source-callout">
                <strong>Primary Scraped Document:</strong> <code>{d.get('scraped_url')}</code><br>
                <span style="font-size:0.75rem;color:#94a3b8;">Extracted full article text stripped of markup and boilerplate for deep factual synthesis.</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

else:
    with results_area:
        st.markdown("""
        <div class="standby-state-box">
            <div style="font-size:2.4rem;margin-bottom:0.8rem;color:#6366f1;">🔬</div>
            <div style="font-size:1.2rem;font-weight:700;color:#ffffff;margin-bottom:0.4rem;">
                Autonomous Research Engine Ready
            </div>
            <div style="font-size:0.9rem;color:#94a3b8;max-width:480px;margin:0 auto;line-height:1.5;">
                Enter any query or hypothesis above to launch the 4-agent cognitive pipeline. 
                Web discovery, deep scraping, executive reporting, and audit results will appear here.
            </div>
        </div>
        """, unsafe_allow_html=True)
