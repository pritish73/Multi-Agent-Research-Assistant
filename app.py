import streamlit as st
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🔎", layout="wide")

st.title("Multi-Agent Research Assistant")
st.caption("Search agent → Reader agent → Writer chain → Critic chain")

if "state" not in st.session_state:
    st.session_state.state = {}

topic = st.text_input("Research topic", placeholder="e.g. Latest advances in solid-state batteries")
run_clicked = st.button("Run Research", type="primary", disabled=not topic.strip())

if run_clicked:
    state = {}

    # ---------- Step 1: Search agent ----------
    with st.status("Step 1 · Search agent is working...", expanded=True) as status:
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = search_result["messages"][-1].content
        st.markdown(state["search_results"])
        status.update(label="Step 1 · Search complete", state="complete", expanded=False)

    # ---------- Step 2: Reader agent ----------
    with st.status("Step 2 · Reader agent is scraping top resources...", expanded=True) as status:
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state["scraped_content"] = reader_result["messages"][-1].content
        st.markdown(state["scraped_content"])
        status.update(label="Step 2 · Scraping complete", state="complete", expanded=False)

    # ---------- Step 3: Writer chain ----------
    with st.status("Step 3 · Writer is drafting the report...", expanded=True) as status:
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']} \n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })
        st.markdown(state["report"])
        status.update(label="Step 3 · Draft complete", state="complete", expanded=False)

    # ---------- Step 4: Critic chain ----------
    with st.status("Step 4 · Critic is reviewing the report...", expanded=True) as status:
        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })
        st.markdown(state["feedback"])
        status.update(label="Step 4 · Review complete", state="complete", expanded=False)

    st.session_state.state = state
    st.success("Research pipeline finished!")

# ---------- Results (persist across reruns) ----------
state = st.session_state.state
if state:
    st.divider()
    st.header("Final Report")
    st.markdown(state.get("report", "_No report yet._"))

    with st.expander(" Critic feedback"):
        st.markdown(state.get("feedback", ""))

    with st.expander(" Raw search results"):
        st.markdown(state.get("search_results", ""))

    with st.expander(" Scraped content"):
        st.markdown(state.get("scraped_content", ""))

    st.download_button(
        "Download report (.md)",
        data=state.get("report", ""),
        file_name="research_report.md",
        mime="text/markdown",
    )
