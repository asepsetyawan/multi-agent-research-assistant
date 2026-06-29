import streamlit as st

from research_assistant.graph.workflow import run_research


st.set_page_config(page_title="Multi-Agent Research Assistant", layout="wide")
st.title("Multi-Agent Research Assistant")
st.caption("Planner → Researchers (parallel) → Critic → Writer, powered by LangGraph")

question = st.text_area(
  "Research question",
  placeholder="e.g. What are the trade-offs between RAG and fine-tuning for enterprise QA?",
  height=100,
)

if st.button("Run research", type="primary", disabled=not question.strip()):
  with st.spinner("Agents are collaborating..."):
    try:
      result = run_research(question.strip())
    except Exception as exc:
      st.error(f"Research failed: {exc}")
      st.stop()

  st.subheader("Subtasks")
  for subtask in result.get("subtasks", []):
    st.markdown(f"- {subtask}")

  with st.expander("Research notes", expanded=False):
    for item in result.get("research_results", []):
      st.markdown(f"### {item['subtask']}")
      st.write(item["summary"])
      for source in item.get("sources", []):
        st.markdown(f"- [{source['title']}]({source['url']})")

  st.subheader("Critique")
  st.info(result.get("critique", "No critique generated."))

  st.subheader("Final report")
  st.markdown(result.get("report", "No report generated."))
