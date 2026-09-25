import html
import os

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from agents import build_reader_agent, build_search_agent, run_writer, run_critic


app = FastAPI(title="Multi-Agent Research Assistant")


PAGE = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Multi-Agent Research Assistant</title>
<style>
body{{font-family:Arial,sans-serif;max-width:1000px;margin:40px auto;padding:0 20px;background:#0b0f19;color:#eee}}
.card{{background:#151b2b;border:1px solid #29334d;border-radius:16px;padding:24px;margin:18px 0}}
input{{width:70%;padding:14px;border-radius:10px;border:1px solid #39445f;background:#0f1421;color:#fff}}
button{{padding:14px 20px;border:0;border-radius:10px;background:#6d5dfc;color:white;font-weight:700;cursor:pointer}}
pre{{white-space:pre-wrap;line-height:1.55}}
h1{{margin-bottom:8px}}.muted{{color:#9aa5bd}}
</style>
</head>
<body>
<h1>🔎 Multi-Agent Research Assistant</h1>
<p class="muted">Search Agent → Reader Agent → Writer → Critic</p>
<form method="post">
<div class="card">
<input name="topic" placeholder="e.g. Latest advances in solid-state batteries" value="{topic}">
<button>Run Research</button>
</div>
</form>
{result}
</body></html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE.format(topic="", result="")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mistral_key_configured": bool(os.getenv("MISTRAL_API_KEY")),
        "tavily_key_configured": bool(os.getenv("TAVILY_API_KEY")),
    }


@app.post("/", response_class=HTMLResponse)
def research(topic: str = Form(...)):
    topic = topic.strip()

    if not topic:
        return PAGE.format(
            topic="",
            result="<div class='card'>Enter a research topic.</div>"
        )

    try:
        if not os.getenv("MISTRAL_API_KEY"):
            raise RuntimeError(
                "MISTRAL_API_KEY is not configured. Add it to your Vercel Environment Variables."
            )

        if not os.getenv("TAVILY_API_KEY"):
            raise RuntimeError(
                "TAVILY_API_KEY is not configured. Add it to your Vercel Environment Variables."
            )

        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [
                ("user", f"Find recent, reliable and detailed information about: {topic}")
            ]
        })
        search_text = search_result["messages"][-1].content

        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [(
                "user",
                f"Based on these search results about '{topic}', pick the most relevant URL "
                f"and scrape it for deeper content.\n\nSearch Results:\n{search_text[:8000]}"
            )]
        })
        scraped = reader_result["messages"][-1].content

        combined = (
            f"SEARCH RESULTS:\n{search_text}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{scraped}"
        )

        report = run_writer(topic, combined)
        feedback = run_critic(report)

        result = f"""
        <div class="card"><h2>Final Report</h2><pre>{html.escape(report)}</pre></div>
        <div class="card"><h2>Critic Feedback</h2><pre>{html.escape(feedback)}</pre></div>
        <div class="card"><h2>Search Results</h2><pre>{html.escape(search_text)}</pre></div>
        """

        return PAGE.format(
            topic=html.escape(topic),
            result=result
        )

    except Exception as e:
        return PAGE.format(
            topic=html.escape(topic),
            result=(
                "<div class='card'><h2>Runtime error</h2>"
                f"<pre>{html.escape(str(e))}</pre></div>"
            )
        )
