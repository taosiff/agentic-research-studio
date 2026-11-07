import os
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
