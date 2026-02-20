import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_community.tools.arxiv.tool import ArxivQueryRun
import pymupdf4llm

# Define the shared state
class AgentState(TypedDict):
    pdf_text: str
    core_claims: List[str]
    equations: List[str]
    baselines: List[str]
    critique: str
    revision_needed: bool

# Agent A: The Reader
def reader_agent(state: AgentState):
    # In a real app, this would take the uploaded file path
    # md_text = pymupdf4llm.to_markdown("paper.pdf")
    return {"core_claims": ["Claim 1: Faster Convergence"], "equations": ["$L = \sum (y - \hat{y})^2$"]}

# Agent B: The Scholar (Using ArXiv API)
def scholar_agent(state: AgentState):
    # Logic to search ArXiv for existing baselines from 2024-2025
    return {"baselines": ["Model X (2024)", "Method Y (2025)"]}

# Agent C: The Critic (Chain-of-Thought)
def critic_agent(state: AgentState):
    llm = ChatOpenAI(model="gpt-4-turbo-preview")
    prompt = f"Analyze these claims: {state['core_claims']} against these equations {state['equations']}. Check for N-value significance."
    response = llm.invoke(prompt)
    return {"critique": response.content, "revision_needed": False}

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("reader", reader_agent)
workflow.add_node("scholar", scholar_agent)
workflow.add_node("critic", critic_agent)

workflow.set_entry_point("reader")
workflow.add_edge("reader", "scholar")
workflow.add_edge("scholar", "critic")
workflow.add_edge("critic", END)

executor = workflow.compile()
