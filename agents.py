from functools import lru_cache

from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url


@lru_cache(maxsize=1)
def get_llm():
    # Mistral can return HTTP 429 when several agent stages run close together.
    # Let the client retry transient failures with exponential backoff.
    return ChatMistralAI(
        model="mistral-small-2506",
        max_retries=5,
        timeout=60,
        max_tokens=1200,
        temperature=0.2,
    )


def build_search_agent():
    return create_agent(
        model=get_llm(),
        tools=[web_search]
    )


def build_reader_agent():
    return create_agent(
        model=get_llm(),
        tools=[scrape_url]
    )


writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured and insightful reports."
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""
    ),
])


critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive research critic. Be honest and specific."
    ),
    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""
    ),
])


def run_writer(topic, research):
    return (writer_prompt | get_llm() | StrOutputParser()).invoke({
        "topic": topic,
        "research": research
    })


def run_critic(report):
    return (critic_prompt | get_llm() | StrOutputParser()).invoke({
        "report": report
    })
