import os
import re
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

def get_groq_llm(model_name: str = None, temperature: float = 0.1):
    model = model_name or os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    return ChatGroq(
        model=model,
        temperature=temperature,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

llm = get_groq_llm()

def execute_search_agent(topic: str, custom_llm=None) -> dict:
    active_llm = custom_llm or llm
    
    query_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional research query strategist. Generate ONLY a single, high-precision web search query for the given topic. Return ONLY the raw query string without quotes, punctuation, or preamble."),
        ("human", "{topic}")
    ])
    query_chain = query_prompt | active_llm | StrOutputParser()
    try:
        search_query = query_chain.invoke({"topic": topic}).strip().strip('"').strip("'")
    except Exception:
        search_query = topic

    search_raw = web_search.invoke({"query": search_query})

    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an intelligence researcher. Summarize the key findings from these web search results into concise bullet points, highlighting verified facts and notable sources."),
        ("human", "Topic: {topic}\n\nSearch Results:\n{search_results}")
    ])
    summary_chain = summary_prompt | active_llm | StrOutputParser()
    try:
        summary = summary_chain.invoke({"topic": topic, "search_results": search_raw[:2500]})
    except Exception:
        summary = search_raw[:1500]

    return {
        "query": search_query,
        "raw": search_raw,
        "summary": summary
    }

def execute_reader_agent(topic: str, search_raw: str, custom_llm=None) -> dict:
    active_llm = custom_llm or llm

    url_prompt = ChatPromptTemplate.from_messages([
        ("system", "From the search results below, identify and select the single most authoritative, primary, and relevant URL to scrape for deeper factual context. Return ONLY the exact raw URL (e.g. https://...). Do not include explanations."),
        ("human", "Topic: {topic}\n\nSearch Results:\n{search_results}")
    ])
    url_chain = url_prompt | active_llm | StrOutputParser()
    
    try:
        chosen_text = url_chain.invoke({"topic": topic, "search_results": search_raw[:2000]}).strip()
        found_urls = re.findall(r'https?://[^\s\)\"\']+', chosen_text)
        target_url = found_urls[0] if found_urls else None
    except Exception:
        target_url = None

    if not target_url:
        all_urls = re.findall(r'https?://[^\s\)\"\']+', search_raw)
        target_url = all_urls[0] if all_urls else ""

    if target_url:
        scraped_text = scrape_url.invoke({"url": target_url})
    else:
        scraped_text = "No accessible URL found in search results to scrape."

    return {
        "url": target_url,
        "content": scraped_text
    }

def build_search_agent(custom_llm=None):
    return create_agent(
        model=custom_llm or llm,
        tools=[web_search],
    )

def build_reader_agent(custom_llm=None):
    return create_agent(
        model=custom_llm or llm,
        tools=[scrape_url],
    )

def build_writer_chain(custom_llm=None):
    active_llm = custom_llm or llm
    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an elite research analyst and writer. Your job is to synthesize raw multi-source intelligence into high-impact, deeply informative, and beautifully structured reports."),
        ("human", """Write an authoritative, comprehensive research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report clearly in Markdown:
# [Clear, Engaging Report Title]

## Executive Summary
[A high-level synthesis of key insights, trends, and significance]

## Key Findings & Core Pillars
[Provide 3 to 4 well-developed findings with actionable detail, context, and data points]

## Deep Dive Analysis & Market Implications
[Examine drivers, challenges, impact on stakeholders, and strategic foresight]

## Future Outlook & Roadmap
[Projected developments, emerging milestones, and expectations]

## Key Takeaways
[3-5 bulleted summary takeaways]

## Verified Sources & References
[List all extracted URLs and source citations gathered during research]

Maintain an analytical, objective, and deeply informative tone."""),
    ])
    return writer_prompt | active_llm | StrOutputParser()

writer_chain = build_writer_chain()

def build_critic_chain(custom_llm=None):
    active_llm = custom_llm or llm
    critic_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a distinguished peer reviewer and principal research auditor. You rigorously evaluate report completeness, factual soundness, logical structure, and clarity."),
        ("human", """Review the research report below and provide a concise, sharp critical evaluation.

Report:
{report}

Provide your evaluation in this exact clean markdown format:

### 📊 Review Score: [X/10]

#### ✨ Key Strengths
- **[Strength 1]**: [Detail]
- **[Strength 2]**: [Detail]

#### ⚠️ Areas for Expansion & Caution
- **[Critique 1]**: [Detail]
- **[Critique 2]**: [Detail]

#### 🎯 Auditor Verdict
[A 2-3 sentence definitive verdict on the publication readiness and credibility of the analysis]"""),
    ])
    return critic_prompt | active_llm | StrOutputParser()

critic_chain = build_critic_chain()
