from src.agents.agents import (
    execute_search_agent,
    execute_reader_agent,
    writer_chain,
    critic_chain
)
from rich import print as rprint

def run_research_pipeline(topic: str) -> dict:
    state = {}

    rprint("\n[bold cyan]" + "="*60 + "[/bold cyan]")
    rprint(f"[bold white]🚀 Launching Autonomous Research Pipeline for:[/bold white] [bold yellow]{topic}[/bold yellow]")
    rprint("[bold cyan]" + "="*60 + "[/bold cyan]\n")

    rprint("[bold blue]✦ Step 1:[/bold blue] Search Agent gathering intelligence via Tavily...")
    search_data = execute_search_agent(topic)
    state["search_results"] = search_data["summary"]
    state["search_raw"] = search_data["raw"]
    rprint("[green]✔ Step 1 complete: Search results acquired.[/green]\n")

    rprint("[bold blue]✦ Step 2:[/bold blue] Reader Agent inspecting top sources & scraping in-depth content...")
    reader_data = execute_reader_agent(topic, search_data["raw"])
    state['scraped_content'] = reader_data["content"]
    state['scraped_url'] = reader_data["url"]
    rprint(f"[green]✔ Step 2 complete: Web source content extracted from {reader_data['url']}.[/green]\n")

    rprint("[bold blue]✦ Step 3:[/bold blue] Writer Agent synthesizing report with Groq LLM...")
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    rprint("[green]✔ Step 3 complete: Draft report generated.[/green]\n")

    rprint("[bold blue]✦ Step 4:[/bold blue] Critic Agent auditing report quality and scoring...")
    state["feedback"] = critic_chain.invoke({
        "report": state['report']
    })
    rprint("[green]✔ Step 4 complete: Critic evaluation finished.[/green]\n")

    rprint("[bold green]" + "="*60 + "[/bold green]")
    rprint("[bold green]✔ Autonomous Research Pipeline Completed Successfully![/bold green]")
    rprint("[bold green]" + "="*60 + "[/bold green]\n")

    return state
